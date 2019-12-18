#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
import web
import time
from bson.objectid import ObjectId
from config import setting
import helper

db = setting.db_web

# 问题提交编辑，只能问题提交人修改，其他人跟贴

url = ('/ticket/edit')

class handler:

    def GET(self):
        if not helper.logged(helper.PRIV_USER, 'TICKET_OP'):
            raise web.seeother('/')

        render = helper.create_render()
        user_data = web.input(ticket_id='')

        # 用户列表, 及东华用户列表
        user_list = {}
        db_user=db.user.find({})
        for u in db_user:
            if u['login']==0:
                continue
            if 'TICKET_OP' in helper.get_privilege_name(u['privilege'], u['menu_level']):
                user_list[u['uname']] = u['full_name']

        # 准备数据
        ticket_data = { 'ticket_id' : 'n/a', 'status' : 'OPEN' }
        image_list = []

        if user_data.ticket_id != '': # 现有记录
            db_obj=db.ticket.find_one({'_id':ObjectId(user_data.ticket_id)})

            if db_obj!=None:
                # 已存在的obj
                ticket_data = db_obj
                ticket_data['ticket_id']=ticket_data['_id']

                # 只有提交和处理才能修改
                if ticket_data['open_uid']!=helper.get_session_uname() and ticket_data['killer_uid']!=helper.get_session_uname():
                    return render.info('不是提交人或处理人，不能修改！')  

                for x in db_obj.get('images', []):
                    r2 = db.base_image.find_one({'image':x})
                    if r2:
                        image_list.append((x, r2['file']))

        # 对于只保存一半数据的记录处理
        ticket_data['open_uid'] = helper.get_session_uname()
        ticket_data['open_name'] = user_list[helper.get_session_uname()]

        return render.ticket_edit(helper.get_session_uname(), helper.get_privilege_name(), 
            ticket_data, user_list, helper.TICKET_TYPE, helper.TICKET_SOURCE, helper.TICKET_STATUS, image_list)


    def POST(self):
        if not helper.logged(helper.PRIV_USER, 'TICKET_OP'):
            raise web.seeother('/')

        render = helper.create_render()
        user_data=web.input(ticket_id='', title='', status='')

        #print user_data
        
        title = user_data.title.strip()
        if title=='':
            return render.info('标题不能为空！')  

        if user_data['category']=='':
            return render.info('问题类型不能为空！')  

        if user_data['source']=='':
            return render.info('问题来源不能为空！')  

        status = user_data.status.strip()
        if status=='':
            return render.info('问题状态不能为空！')  

        if user_data['killer_uid']=='':
            return render.info('问题处理人不能为空！')  

        if user_data['ticket_id']=='n/a': # 新建
            ticket_id = None
            message = '新建问题'
        else:
            ticket_id = ObjectId(user_data['ticket_id'])
            message = '修改问题'


        try:
            update_set={
                'title'      : title,
                'status'     : status,
                'category'   : int(user_data['category']),
                'source'     : int(user_data['source']),
                'detail'     : user_data['detail'],
                'submitter'  : user_data['submitter'],
                'plan_date'  : user_data['plan_date'],
                'killer_uid' : user_data['killer_uid'],
                'images'      : user_data['image'].split(','), # 上传文件
                'last_date'  : helper.time_str(),
                'last_tick'  : int(time.time()),  # 更新时间戳
            }
        except ValueError:
            return render.info('请在相应字段输入数字！')


        if ticket_id is None: #新建
            # 取得sku计数
            db_pk = db.user.find_one_and_update(
                {'uname'    : 'settings'},
                {'$inc'     : {'pk_count' : 1}},
                {'pk_count' : 1}
            )
            update_set['ticket_no'] = db_pk['pk_count'] # 新建增加 ticket_no
            update_set['open_uid'] = helper.get_session_uname()
            update_set['first_date'] = helper.time_str() 
            update_set['first_t'] = int(time.time())
            update_set['history'] = [(helper.time_str(), helper.get_session_uname(), message)]
            r2 = db.ticket.insert_one(update_set)
        else:
            db.ticket.update_one({'_id':ticket_id}, {
                '$set'  : update_set,
                '$push' : {
                    'history' : (helper.time_str(), helper.get_session_uname(), message), 
                }  # 纪录操作历史
            })

        # 
        return render.info('成功保存！', '/ticket/list')
