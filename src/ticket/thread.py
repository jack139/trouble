#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
import web
import time
from bson.objectid import ObjectId
from config import setting
import helper

db = setting.db_web

# 问题帖子，可跟贴，原问题/状态修改 只限 提交人和处理人，其他人可 跟帖 写意见

url = ('/ticket/thread')

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

        if user_data.ticket_id == '': 
            return render.info('参数错误！')  

        db_obj=db.ticket.find_one({'_id':ObjectId(user_data.ticket_id)})
        if db_obj is None:
            return render.info('未找到数据！')  

        # 已存在的obj
        ticket_data = db_obj
        ticket_data['ticket_id']=ticket_data['_id']

        # 处理问题里的附件
        for x in db_obj.get('images', []):
            r2 = db.base_image.find_one({'image':x})
            if r2:
                image_list.append((x, r2['file']))      

        # 处理回复帖子里的附件
        for xx in db_obj.get('follow_list', []):
            xx['image_list'] = []
            for x in xx.get('images', []):
                r2 = db.base_image.find_one({'image':x})
                if r2:
                    xx['image_list'].append((x, r2['file']))      

        # 对于只保存一半数据的记录处理
        ticket_data['open_name'] = user_list[ticket_data['open_uid']]

        return render.ticket_thread(helper.get_session_uname(), helper.get_privilege_name(), 
            ticket_data, user_list, helper.TICKET_TYPE, helper.TICKET_SOURCE, helper.TICKET_STATUS, image_list)


