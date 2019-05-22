#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
import web
import time
from bson.objectid import ObjectId
from config import setting
import helper

db = setting.db_web

# 删除记录

url = ('/duty/remove')

class handler:

    def GET(self):
        if not helper.logged(helper.PRIV_USER, 'ONDUTY'):
            raise web.seeother('/')

        render = helper.create_render()
        user_data = web.input(duty_id='')

        if user_data.duty_id == '': 
            return render.info('参数错误！')  

        r2 = db.duty.find_one({'_id':ObjectId(user_data.duty_id)})
        if r2 is None:
            return render.info('为未找到值班记录！')  

        if r2['status_duty']!='SAVED':
            return render.info('只有未提交的记录可以删除！')  

        if r2['duty_uid']!=helper.get_session_uname():
            return render.info('只能删除自己的值班记录！')  

        db.duty.delete_one({'_id':ObjectId(user_data.duty_id)})

        return render.info('成功删除！', '/duty/list')

