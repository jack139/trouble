#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
import web
import time
from bson.objectid import ObjectId
from config import setting
import helper

db = setting.db_web

# 交接记录

url = ('/duty/finish')

class handler:

    def POST(self):
        if helper.logged(helper.PRIV_USER, 'ONDUTY'):
            ROLE = 'ONDUTY'
        elif helper.logged(helper.PRIV_USER, 'DHCDUTY'):
            ROLE = 'DHCDUTY'
        else:
            raise web.seeother('/')

        render = helper.create_render()
        user_data = web.input(duty_id='')

        if user_data.duty_id == '': 
            return render.info('参数错误！')  

        r2 = db.duty.find_one({'_id':ObjectId(user_data.duty_id)})
        if r2 is None:
            return render.info('为未找到值班记录！')  

        if ROLE == 'ONDUTY':
            if r2['status_duty']!='CLOSED':
                return render.info('只有已提交的记录可以交接！')  

            if r2['next_uid']!=helper.get_session_uname():
                return render.info('只能交接本人是交接人的值班记录！')  

            try:
                update_set={
                        'status_key'   : int(user_data.get('status_key',0)), 
                        'status_phone' : int(user_data.get('status_phone',0)), 

                        'status_duty'  : 'FINISHED',
                        'finish_t'     : helper.time_str(),
                }
            except ValueError:
                return render.info('请在相应字段输入数字！')

            db.duty.update_one({'_id':ObjectId(user_data.duty_id)}, {
                '$set'  : update_set,
                '$push' : {
                    'history' : (helper.time_str(), helper.get_session_uname(), '交接'), 
                }  # 纪录操作历史
            })

        else:
            if r2['dhc_status_duty']!='CLOSED':
                return render.info('只有已提交的记录可以交接！')  

            if r2['dhc_next_uid']!=helper.get_session_uname():
                return render.info('只能交接本人是交接人的值班记录！')  

            try:
                update_set={
                        'dhc_status_duty'  : 'FINISHED',
                        'dhc_finish_t'     : helper.time_str(),
                }
            except ValueError:
                return render.info('请在相应字段输入数字！')

            db.duty.update_one({'_id':ObjectId(user_data.duty_id)}, {
                '$set'  : update_set,
                '$push' : {
                    'history' : (helper.time_str(), helper.get_session_uname(), '交接'), 
                }  # 纪录操作历史
            })


        return render.info('交接完成！', '/duty/list')

