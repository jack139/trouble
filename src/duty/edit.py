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
        if not helper.logged(helper.PRIV_USER, 'DATA_MODIFY'):
            raise web.seeother('/')
        render = helper.create_render()
        user_data=web.input(duty_id='', rule_name='')

        rule_name = user_data.rule_name.strip()
        if rule_name=='':
            return render.info('规则名不能为空！')  

        # 排除规则同名
        find_condition = {
            'rule_name'  : rule_name,
        }

        if user_data['duty_id']=='n/a': # 新建
            duty_id = None
            message = '新建'
        else:
            duty_id = ObjectId(user_data['duty_id'])
            message = '修改'
            find_condition['_id'] = { '$ne' : duty_id}  # 排除自己

        r1 = db.bayes.find_one(find_condition)
        if r1 is not None:
            return render.info('规则名已存在，不能重复！')  


        try:
            update_set={
                'rule_name'  : rule_name,
                'key_word'   : user_data['key_word'], 
                'reply'      : user_data['reply'],
                'reply_type' : int(user_data['reply_type']),
                'available'  : int(user_data['available']),
                'last_tick'  : int(time.time()),  # 更新时间戳
            }
        except ValueError:
            return render.info('请在相应字段输入数字！')

        if duty_id is None:
            update_set['history'] = [(helper.time_str(), helper.get_session_uname(), message)]
            r2 = db.bayes.insert_one(update_set)
        else:
            db.bayes.update_one({'_id':duty_id}, {
                '$set'  : update_set,
                '$push' : {
                    'history' : (helper.time_str(), helper.get_session_uname(), message), 
                }  # 纪录操作历史
            })

        # 重新计算规则
        from libs import bayes_helper
        if bayes_helper.trainToDB() is None:
            return render.info('规则计算出错！', '/plat/bayes_edit?duty_id='+user_data['duty_id'])            
        else:
            return render.info('成功保存！', '/plat/bayes')
