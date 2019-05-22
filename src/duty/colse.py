#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
import web
import time
from bson.objectid import ObjectId
from config import setting
import helper

db = setting.db_web

# 提交记录

url = ('/duty/close')

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
            return render.info('只有未提交的记录可以提交！')  

        if r2['duty_uid']!=helper.get_session_uname():
            return render.info('只能提交本人的值班记录！')  

        if -1 in (r2['room1_device'], r2['room2_device'], r2['room1_ups'], r2['room2_ups'], r2['room1_conditioner'], 
            r2['room2_conditioner'], r2['system_big_issue']):
            return render.info('有未填单选项，请填写后保存，然后再提交！') 

        if '' in (r2['room1_temp_humi1']['temp'], r2['room1_temp_humi1']['humi'], 
            r2['room1_temp_humi2']['temp'], r2['room1_temp_humi2']['humi'], 
            r2['room2_temp_humi']['temp'], r2['room2_temp_humi']['humi'] ):
            return render.info('有未填数据，请填写后保存，然后再提交！') 

        db.duty.update_one({'_id':ObjectId(user_data.duty_id)}, {
            '$set'  : {
                'status_duty' : 'CLOSED',
                'close_t'     : helper.time_str(),
            },
            '$push' : {
                'history' : (helper.time_str(), helper.get_session_uname(), '提交'), 
            }  # 纪录操作历史
        })

        return render.info('成功提交！', '/duty/list')

