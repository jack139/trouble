#!/usr/bin/env python
# -*- coding: utf-8 -*-

import web
from config import setting
import helper

db = setting.db_web

PAGE_SIZE = 25

url = ('/ticket/list')

# - 已填报信息列表 －－－－－－－－－－－
class handler:      
    def GET(self):
        if not helper.logged(helper.PRIV_USER,'TICKET_OP'):
            raise web.seeother('/')

        render = helper.create_render()
        user_data=web.input(page='0', name='', search_title='', search_type='', search_status='', search_uid='')

        if not user_data['page'].isdigit():
            return render.info('参数错误！')  


        conditions ={}

        search_name = user_data.search_title.strip()
        if search_name!='':
            if search_name[0]=='#' and search_name[1:].isdigit():
                conditions['ticket_no'] = int(search_name[1:])
            else:
                conditions['title'] = { '$regex' : u'%s.*'%(search_name.replace('*','\\*').replace('?','\\?')), '$options' : 'i' }

        search_type = user_data.search_type.strip()
        if search_type!='':
            conditions['category'] = int(search_type)

        search_status = user_data.search_status.strip()
        if search_status!='':
            conditions['status'] = search_status

        search_uid = user_data.search_uid.strip()
        if search_uid!='':
            conditions['killer_uid'] = search_uid

        # 用户列表, 及东华用户列表
        user_list = {}
        db_user=db.user.find({})
        for u in db_user:
            if u['login']==0:
                continue
            if 'TICKET_OP' in helper.get_privilege_name(u['privilege'], u['menu_level']):
                user_list[u['uname']] = u['full_name']

        # 分页获取数据
        db_sku = db.ticket.find(conditions,
            sort=[('_id', -1)],
            limit=PAGE_SIZE,
            skip=int(user_data['page'])*PAGE_SIZE
        )

        num = db_sku.count()
        if num%PAGE_SIZE>0:
            num = num / PAGE_SIZE + 1
        else:
            num = num / PAGE_SIZE


        return render.ticket_list(helper.get_session_uname(), helper.get_privilege_name(), 
            range(0, num), db_sku, int(user_data['page']), search_name, search_type, search_status, search_uid,
            helper.TICKET_TYPE,  helper.TICKET_STATUS, user_list)



