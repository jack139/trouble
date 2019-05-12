#!/usr/bin/env python
# -*- coding: utf-8 -*-

import web
from bson.objectid import ObjectId
from config import setting
import helper

db = setting.db_web


url = ('/ticket/detail')

# - 填报详细信息 －－－－－－－－－－－
class handler:      
    def GET(self):
        if not helper.logged(helper.PRIV_USER,'JOB_LIST'):
            raise web.seeother('/')

        render = helper.create_render()
        user_data=web.input(id='')

        if user_data['id']=='':
            return render.info('参数错误！')  

        # 分页获取数据
        db_sku = db.job_sheet.find_one({'_id':ObjectId(user_data['id'])})
        if db_sku is None:
            return render.info('信息不存在！')  

        image_list = []
        for x in db_sku.get('image', []):
            r2 = db.base_image.find_one({'image':x})
            if r2:
                image_list.append((x, r2['file']))

        return render.job_detail(helper.get_session_uname(), helper.get_privilege_name(), 
            db_sku, image_list)



