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
        if helper.logged(helper.PRIV_USER, 'ONDUTY'):
            ROLE = 'ONDUTY'
        elif helper.logged(helper.PRIV_USER, 'DHCDUTY'):
            ROLE = 'DHCDUTY'
        else:
            raise web.seeother('/')

        print 'ROLE:', ROLE

        render = helper.create_render()
        user_data = web.input(duty_id='')

        # 用户列表, 及东华用户列表
        user_list = {}
        dhc_user_list = {}
        db_user=db.user.find({})
        for u in db_user:
            if u['login']==0:
                continue
            if 'ONDUTY' in helper.get_privilege_name(u['privilege'], u['menu_level']):
                user_list[u['uname']] = u['full_name']

            if 'DHCDUTY' in helper.get_privilege_name(u['privilege'], u['menu_level']):
                dhc_user_list[u['uname']] = u['full_name']

        # 准备数据
        duty_data = { 'duty_id' : 'n/a', 'status_duty' : 'SAVED' }

        if user_data.duty_id != '': # 现有记录
            db_obj=db.duty.find_one({'_id':ObjectId(user_data.duty_id)})
            if db_obj!=None:
                # 已存在的obj
                duty_data = db_obj
                duty_data['duty_id']=duty_data['_id']
        else: # 新记录
            if ROLE == 'ONDUTY':
                duty_data['duty_uid'] = helper.get_session_uname()
            else:
                duty_data['dhc_duty_uid'] = helper.get_session_uname()
            duty_data['duty_name'] = user_list[helper.get_session_uname()]

        if ROLE == 'ONDUTY' and duty_data['duty_uid']==helper.get_session_uname() and duty_data['status_duty']=='SAVED':
            return render.duty_edit(helper.get_session_uname(), helper.get_privilege_name(), duty_data, user_list, dhc_user_list)
        elif ROLE == 'DHCDUTY' and duty_data.get('dhc_duty_uid')==helper.get_session_uname() and (duty_data.get('dhc_status_duty') in ['SAVED', None]):
            return render.duty_edit(helper.get_session_uname(), helper.get_privilege_name(), duty_data, user_list, dhc_user_list)
        else:
            return render.duty_detail(helper.get_session_uname(), helper.get_privilege_name(), duty_data, user_list, dhc_user_list)


    def POST(self):
        if helper.logged(helper.PRIV_USER, 'ONDUTY'):
            ROLE = 'ONDUTY'
        elif helper.logged(helper.PRIV_USER, 'DHCDUTY'):
            ROLE = 'DHCDUTY'
        else:
            raise web.seeother('/')

        render = helper.create_render()
        user_data=web.input(duty_id='', duty_uid='', dhc_duty_uid='', duty_date='', next_uid='')

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


        if ROLE == 'ONDUTY': # 信息中心值班人员处理
            if user_data.dhc_duty_uid=='':
                return render.info('东华值班人不能为空！')  

            if user_data.next_uid=='':
                return render.info('交接人不能为空！')  

            try:
                update_set={
                    'duty_date'         : duty_date,
                    'duty_uid'          : user_data['duty_uid'],
                    'dhc_duty_uid'      : user_data['dhc_duty_uid'],
                    'room1_device'      : int(user_data.get('room1_device',-1)), 
                    'room2_device'      : int(user_data.get('room2_device',-1)), 
                    'room1_ups'         : int(user_data.get('room1_ups',-1)), 
                    'room2_ups'         : int(user_data.get('room2_ups',-1)), 
                    'room1_conditioner' : int(user_data.get('room1_conditioner',-1)), 
                    'room2_conditioner' : int(user_data.get('room2_conditioner',-1)), 
                    'room1_temp_humi1'  : { 'temp' : user_data.get('room1_temp1','').strip(), 'humi' : user_data.get('room1_humi1','').strip()}, 
                    'room1_temp_humi2'  : { 'temp' : user_data.get('room1_temp2','').strip(), 'humi' : user_data.get('room1_humi2','').strip()}, 
                    'room2_temp_humi'   : { 'temp' : user_data.get('room2_temp','').strip(), 'humi' : user_data.get('room2_humi','').strip()}, 
                    'device_issue'      : user_data['device_issue'].strip(),
                    'device_solution'   : user_data['device_solution'].strip(),
                    
                    'system_big_issue'  : int(user_data.get('system_big_issue',-1)), 
                    'system_issue'      : user_data['system_issue'].strip(),
                    'system_solution'   : user_data['system_solution'].strip(),

                    'duty_log'          : user_data['duty_log'].strip(),

                    'status_key'        : int(user_data.get('status_key',0)), 
                    'status_phone'      : int(user_data.get('status_phone',0)), 

                    'next_uid'          : user_data['next_uid'],

                    'status_duty'       : 'SAVED',
                    'save_t'            : helper.time_str(),

                    'last_tick'         : int(time.time()),  # 更新时间戳
                }
            except ValueError:
                return render.info('请在相应字段输入数字！')

        else: # 东华值班人员处理
            if user_data.dhc_next_uid=='':
                return render.info('交接人不能为空！')  

            try:
                update_set={
                    'duty_date'         : duty_date,
                    'dhc_duty_uid'      : user_data['dhc_duty_uid'],
                    'dhc_duty_log'      : user_data['dhc_duty_log'].strip(),
                    'dhc_next_uid'      : user_data['dhc_next_uid'],
                    'dhc_status_duty'   : 'SAVED',

                    'dhc_save_t'            : helper.time_str(),
                    'dhc_last_tick'         : int(time.time()),  # 更新时间戳
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
