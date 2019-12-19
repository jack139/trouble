#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
import web
import time
from bson.objectid import ObjectId
from config import setting
import helper

db = setting.db_web

# 问题处理跟贴编辑

url = ('/ticket/follow')

class handler:

    def GET(self):
        if not helper.logged(helper.PRIV_USER, 'TICKET_OP'):
            raise web.seeother('/')

        render = helper.create_render()
        user_data = web.input(ticket_id='',follow_id='')

        if user_data.ticket_id=='':
            return render.info('参数错误！')  

        # 用户列表, 及东华用户列表
        user_list = {}
        db_user=db.user.find({})
        for u in db_user:
            if u['login']==0:
                continue
            if 'TICKET_OP' in helper.get_privilege_name(u['privilege'], u['menu_level']):
                user_list[u['uname']] = u['full_name']

        # 准备数据
        follow_data = { 'follow_id' : 'n/a' }
        image_list = []

        db_obj=db.ticket.find_one({'_id':ObjectId(user_data.ticket_id)})

        if db_obj is None:
            return render.info('未找到问题数据！')  

        follow_list = db_obj.get('follow_list')

        if user_data['follow_id'].isdigit() and len(follow_list)>int(user_data['follow_id']):  # 修改帖子
            # 已存在的follow
            follow_id = int(user_data['follow_id'])
            follow_data = follow_list[follow_id]
            follow_data['follow_id']=follow_id

            # 只有回复人本人才能修改
            if follow_data['follow_uid']!=helper.get_session_uname():
                return render.info('不是回复人本人，不能修改！')  


        follow_data['ticket_id'] = user_data.ticket_id

        for x in follow_data.get('images', []):
            r2 = db.base_image.find_one({'image':x})
            if r2:
                image_list.append((x, r2['file']))

        # 对于只保存一半数据的记录处理
        follow_data['follow_uid'] = helper.get_session_uname()
        follow_data['follow_name'] = user_list[helper.get_session_uname()]

        return render.ticket_follow(helper.get_session_uname(), helper.get_privilege_name(), 
            follow_data, image_list, user_list)


    def POST(self):
        if not helper.logged(helper.PRIV_USER, 'TICKET_OP'):
            raise web.seeother('/')

        render = helper.create_render()
        user_data=web.input(ticket_id='', follow_id='')

        #print user_data
        
        if user_data['ticket_id']=='':
            return render.info('参数错误！')  

        if user_data['follow_id']=='n/a': # 新建
            follow_id = None
            message = '新建问题回复'
        else:
            follow_id = int(user_data['follow_id'])
            message = '修改问题回复'

        db_obj=db.ticket.find_one({'_id':ObjectId(user_data.ticket_id)}, {'follow_list':1})

        if db_obj is None:
            return render.info('未找到问题数据！')  

        follow_list = db_obj.get('follow_list', [])

        try:
            update_set={
                'detail'     : user_data['detail'],
                'images'     : user_data['image'].split(','), # 上传文件
                'follow_uid' : helper.get_session_uname(),
                'last_date'  : helper.time_str(),
                'last_tick'  : int(time.time()),  # 更新时间戳
            }
        except ValueError:
            return render.info('请在相应字段输入数字！')

        if follow_id is None: # 新建
            update_set['first_date'] = helper.time_str() 
            update_set['first_t'] = int(time.time())
            follow_list.append(update_set)
            #r2 = db.ticket.insert_one(update_set)
        else:
            if len(follow_list)>follow_id:
                update_set['first_date'] = follow_list[follow_id]['first_date']
                update_set['first_t'] = follow_list[follow_id]['first_t']
                follow_list[follow_id] = update_set
            else:
                return render.info('未找到问题回复的数据！')  

        db.ticket.update_one({'_id':ObjectId(user_data.ticket_id)}, {
            '$set'  : {
                'follow_list'      : follow_list,
                'last_follow_tick' : int(time.time()),  # 更新时间戳
            },
            '$push' : {
                'history' : (helper.time_str(), helper.get_session_uname(), message), 
            }  # 纪录操作历史
        })

        # 
        return render.info('成功保存！', '/ticket/thread?ticket_id='+user_data['ticket_id'])
