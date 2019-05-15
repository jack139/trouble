#!/usr/bin/env python
# -*- coding: utf-8 -*-

import web
from config import setting
import helper

db = setting.db_web

PAGE_SIZE = 25

url = ('/duty/list')

# - 值班记录列表 －－－－－－－－－－－
class handler:      
    def GET(self):
        if not helper.logged(helper.PRIV_USER,'ONDUTY'):
            raise web.seeother('/')

        render = helper.create_render()
        user_data=web.input(page='0', name='')

        if not user_data['page'].isdigit():
            return render.info('参数错误！')  


        conditions ={}

        search_name = user_data.name.strip()
        if search_name!='':
            conditions['name'] = { '$regex' : u'%s.*'%(search_name.replace('*','\\*').replace('?','\\?')), '$options' : 'i' }


        # 分页获取数据
        db_sku = db.duty.find(conditions,
            sort=[('_id', -1)],
            limit=PAGE_SIZE,
            skip=int(user_data['page'])*PAGE_SIZE
        )

        num = db_sku.count()
        if num%PAGE_SIZE>0:
            num = num / PAGE_SIZE + 1
        else:
            num = num / PAGE_SIZE


        return render.duty_list(helper.get_session_uname(), helper.get_privilege_name(), 
            range(0, num), db_sku, int(user_data['page']))



