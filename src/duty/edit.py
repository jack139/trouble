#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
import web
import time
from bson.objectid import ObjectId
from config import setting
import helper

db = setting.db_web

# 值班记录编辑，已提交的不能修改

url = ('/duty/edit')

class handler:

    def GET(self):
        if not helper.logged(helper.PRIV_USER, 'ONDUTY'):
            raise web.seeother('/')

        render = helper.create_render()
        user_data = web.input(duty_id='')

        duty_data = { 'duty_id' : 'n/a' }

        if user_data.duty_id != '': 
            db_obj=db.duty.find_one({'_id':ObjectId(user_data.duty_id)})
            if db_obj!=None:
                # 已存在的obj
                duty_data = db_obj
                duty_data['duty_id']=duty_data['_id']

        return render.duty_edit(helper.get_session_uname(), helper.get_privilege_name(), duty_data )


    def POST(self):
        if not helper.logged(helper.PRIV_USER, 'ONDUTY'):
            raise web.seeother('/')
        render = helper.create_render()
        user_data=web.input(duty_id='', duty_name='', duty_date='')

        duty_date = user_data.duty_date.strip()
        if duty_date=='':
            return render.info('日期不能为空！')  

        # 排除规则同名
        find_condition = {
            'duty_date'  : duty_date,
        }

        if user_data['duty_id']=='n/a': # 新建
            duty_id = None
            message = '新建'
        else:
            duty_id = ObjectId(user_data['duty_id'])
            message = '修改'
            find_condition['_id'] = { '$ne' : duty_id}  # 排除自己

        r1 = db.duty.find_one(find_condition)
        if r1 is not None:
            return render.info('值班记录已存在，日期不能重复！')  

        try:
            update_set={
                'duty_date'         : duty_date,
                'duty_name'         : user_data['duty_name'],
                'room1_device'      : int(user_data.get('room1_device',-1)), 
                'room2_device'      : int(user_data.get('room2_device',-1)), 
                'room1_ups'         : int(user_data.get('room1_ups',-1)), 
                'room2_ups'         : int(user_data.get('room2_ups',-1)), 
                'room1_conditioner' : int(user_data.get('room1_conditioner',-1)), 
                'room2_conditioner' : int(user_data.get('room2_conditioner',-1)), 
                'room1_temp_humi1'  : { 'temp' : user_data.get('room1_temp1',''), 'humi' : user_data.get('room1_humi1','')}, 
                'room1_temp_humi2'  : { 'temp' : user_data.get('room1_temp2',''), 'humi' : user_data.get('room1_humi2','')}, 
                'room2_temp_humi'   : { 'temp' : user_data.get('room2_temp',''), 'humi' : user_data.get('room2_humi','')}, 
                'device_issue'      : user_data['device_issue'],
                'device_solution'   : user_data['device_solution'],
                
                'system_big_issue'  : int(user_data.get('system_big_issue',-1)), 
                'system_issue'      : user_data['system_issue'],
                'system_solution'   : user_data['system_solution'],

                'duty_log'          : user_data['duty_log'],

                'status_key'        : int(user_data.get('status_key',0)), 
                'status_phone'      : int(user_data.get('status_phone',0)), 

                'status_duty'       : 'SAVED',
                'save_t'            : helper.time_str(),

                'last_tick'         : int(time.time()),  # 更新时间戳
            }
        except ValueError:
            return render.info('请在相应字段输入数字！')

        if duty_id is None:
            update_set['history'] = [(helper.time_str(), helper.get_session_uname(), message)]
            r2 = db.duty.insert_one(update_set)
        else:
            db.duty.update_one({'_id':duty_id}, {
                '$set'  : update_set,
                '$push' : {
                    'history' : (helper.time_str(), helper.get_session_uname(), message), 
                }  # 纪录操作历史
            })

        # 重新计算规则
        return render.info('成功保存！', '/duty/list')
