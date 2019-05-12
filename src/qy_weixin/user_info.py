#!/usr/bin/env python
# -*- coding: utf-8 -*-

import web, json, time, urllib
import app_helper
from libs import qy_helper, app_user_helper

db = app_helper.db

url = ('/qywx/user_info')

def create_render(plain=False):    
    if plain: layout=None
    else: layout='layout'
    render = web.template.render('templates/qy_wx', base=layout)
    return render

def get_career_code(attrs_list):
    career_code = None
    for i in attrs_list:
        if i['name'] == u'学工号':
            career_code = i['value']

    return career_code

# 已参会报名信息
class handler:        
    def GET(self):
        render = create_render(plain=True)
        param = web.input(code='', state='', appid='')

        if param.code!='':
            #if param.appid!=qy_helper.corpid:
            #    return render.info('appid参数错误！')

            if param.state!='PASS':
                return render.info('state参数错误！')

            session_id = qy_helper.init_job(param.code)
            if session_id is not None:
                raise web.seeother('/qywx/user_info?session_id=%s' % session_id)  # 初次进入跳转
            else:
                return render.info('code参数错误！')

        if param.session_id=='':
            return render.info('请用企业维修登录！')

        # session登录后进入
        uname = app_helper.wx_logged(param.session_id)

        if uname is None:
            return render.info('无效的session_id！')

        r2 = app_user_helper.get_user_info(uname['openid'], q_type='openid')
        if r2 is None:
            return render.info('未找到用户信息，请联系管理员！')

        user_info = {
            'career_code' : r2['career_code'],
            'name'        : r2['wx_info']['name'],
            'mobile'      : r2['wx_info']['mobile'],
            'email'       : r2['wx_info']['email'],
            'user_id'     : r2['openid'],
        }

        return render.user_info(param.session_id, user_info)


