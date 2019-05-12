#!/usr/bin/env python
# -*- coding: utf-8 -*-

import web
import time, json, urllib, hashlib
import app_helper
from libs import app_user_helper

from config import setting
db = setting.db_web

REFRESH_HEADIMG = 10 # 更用户头像的频次

corpid = 'wxc10f1e316058780e'
corpsecret = 'rsgchT0XcZoOdHTiKNggOvoLOZ6dWz857cWjox_Jii0' # '翔安医院' app_secret


def get_qy_token(): #  获取企业微信 access_token
    token = get_qy_token0()
    if token is None:
        return get_qy_token0(force=True)
    else:
        return token

def get_qy_token0(force=False, region_id='QY'): # force==True 强制刷新
    print 'region: ', region_id
    if not force:
        db_ticket = db.jsapi_ticket.find_one({'region_id':region_id})
        if db_ticket and int(time.time())-db_ticket.get('token_tick', 0)<3600: # 实际是7200秒过期
            if db_ticket.get('access_token', '')!='':
                print db_ticket['access_token']
                return db_ticket['access_token']
    url='https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=%s&corpsecret=%s' % \
        (corpid, corpsecret)
    f=urllib.urlopen(url)
    data = f.read()
    f.close()

    t=json.loads(data)
    if t.has_key('access_token'):
        print 'ACCESS TOKEN: ', t
        db.jsapi_ticket.update_one({'region_id':region_id},
            {'$set':{'token_tick':int(time.time()), 'access_token':t['access_token']}},upsert=True)
        return t['access_token']
    else:
        print 'FAIL to get ACCESS TOKEN: ', t
        db.jsapi_ticket.update_one({'region_id':region_id},
            {'$set':{'token_tick':int(time.time()), 'access_token':''}},upsert=True)
        return None


# 获取用户基本信息
def get_user_info(openid):
    token = get_qy_token()
    url='https://qyapi.weixin.qq.com/cgi-bin/user/get?access_token=%s&userid=%s' % (token, openid)
    f=urllib.urlopen(url)
    data = f.read()
    f.close()

    print data
    try:
        t=json.loads(data)
    except ValueError:
        t={'errcode':999}
    return t

# 获取教工号
def get_career_code(attrs_list):
    career_code = ''
    for i in attrs_list:
        if i['name'] == u'学工号':
            career_code = i['value']

    return career_code


# 登录入口
def init_job(code):
    if code=='':
        return None

    if code=='test':
        openid = code
    else:
        token = get_qy_token()

        # 读取用户id
        url='https://qyapi.weixin.qq.com/cgi-bin/user/getuserinfo?access_token=%s&code=%s' % \
            (token, code)
        f=urllib.urlopen(url)
        data = f.read()
        f.close()

        t=json.loads(data)
        print t
        if t.has_key('UserId'):
            openid = t['UserId']
        else:
            print 'NOT FOUND: UserId!!!'
            return None


    # 用户基本信息
    info = get_user_info(openid)
    if info['errcode']!=0:
        get_qy_token0(True)
        info = get_user_info(openid)
    print info

    career_code = get_career_code(info['extattr']['attrs'])

    uname = ''
    unionid = ''

    # 检查用户是否已注册
    #db_user = db.app_user .find_one({'openid':openid})
    db_user = app_user_helper.get_user_info(openid, q_type='openid')
    if db_user==None:
        # 未注册，新建用户记录
        new_set = {
            'openid'   : openid,
            'unionid'  : unionid,
            'region_id': 'QY', # 增加 region_id
            'type'     : 'wx_qy', # 用户类型
            'address'  : [],
            #'coupon'   : [], # 送优惠券
            'app_id'   : '', # 微信先注册，没有app_id
            'reg_time' : app_helper.time_str(),
            'wx_nickname'   : info.get('name','未知'),
            'wx_headimgurl' : info.get('avatar', ''),
            'career_code'   : career_code, # 教工号
            'wx_info'       : info,
            'refresh_headimg' : REFRESH_HEADIMG, 
            'last_status' : int(time.time()),
        }
        # 用户中心注册用户接口
        app_user_helper.new_user_info(openid, 'openid', new_set)

    else:
        # 记录今天访问次数
        last_date = db_user.get('last_visit_date')
        today_date = app_helper.time_str(format=1)  # 格式 2016-01-01
        if last_date!=today_date:
            update_set = {
                'last_visit_date' : today_date,
                'today_visit_count' : 1,
                'todat_visit_first_tick' : int(time.time()),
                'todat_push_image_text' : 0,
            }
        else:
            update_set = {
                'today_visit_count' : db_user.get('today_visit_count',0) + 1,
            }

        # 更新 region_id
        if db_user.get('region_id')!='QY':
            update_set['region_id'] = 'QY'


        # 补充用户信息
        update_set['wx_nickname']     = info.get('name','未知')
        update_set['wx_headimgurl']   = info.get('avatar', '')
        update_set['career_code']     = career_code
        update_set['wx_info']         = info

        app_user_helper.update_user_info(openid, q_type='openid', update_set=update_set)


    # 生成 session ------------------

    rand2 = app_helper.my_rand(16)
    now = time.time()
    secret_key = 'f6102bff8451236b8ca1'
    session_id = hashlib.sha1("%s%s%s%s" %(rand2, now, web.ctx.ip.encode('utf-8'), secret_key))
    session_id = session_id.hexdigest()

    db.app_sessions.insert_one({
        'session_id' : session_id,
        'openid'     : openid,
        'unionid'    : unionid,
        'ticket'     : '',
        'uname'      : uname,
        'login'      : 1,
        'rand'       : rand2,
        'ip'         : web.ctx.ip,
        'attime'     : now,
        'type'       : 'wx',
        'career_code': career_code,
    })

    print session_id, openid, uname, career_code
    print "session_id >>>>>>>>>> %r" %session_id
    return session_id



#用户信息返回格式
#{
#    u'telephone': u'', 
#    u'enable': 1, 
#    u'english_name': u'', 
#    u'is_leader_in_dept': [1], 
#    u'isleader': 1, 
#    u'hide_mobile': 0, 
#    u'external_profile': {
#        u'external_corp_name': u'', 
#        u'external_attr': []
#    }, 
#    u'qr_code': u'https://open.work.weixin.qq.com/wwopen/userQRCode?vcode=vc5cd22f99e87a0c8c', 
#    u'department': [573], 
#    u'email': u'tguan@xah.xmu.edu.cn', 
#    u'status': 1, 
#    u'extattr': {
#        u'attrs': [
#            {
#                u'text': {u'value': u'2017710075'}, 
#                u'type': 0, 
#                u'name': u'\u5b66\u5de5\u53f7',  # 学工号
#                u'value': u'2017710075'
#            }, 
#            {
#                u'text': {u'value': u''}, 
#                u'type': 0, 
#                u'name': u'\u767b\u5f55\u540d', # 登录名
#                u'value': u''
#            }, 
#            {
#                u'text': {u'value': u''}, 
#                u'type': 0, 
#                u'name': u'\u82f1\u6587\u540d', # 英文名
#                u'value': u''
#            }
#        ]
#    }, 
#    u'name': u'\u5173\u6d9b', 
#    u'mobile': u'13194084665', 
#    u'gender': u'1', 
#    u'userid': u'tguan@xah', 
#    u'errcode': 0, 
#    u'alias': u'', 
#    u'avatar': u'http://p.qpic.cn/wwhead/duc2TvpEgSTPk74IwG7Bs69yzdkHn4TbqCA6oYeH02kzR2E7t0MhZckyicXEYGwoGwG9agsHicMTw/0', 
#    u'position': u'', 
#    u'order': [0], 
#    u'errmsg': u'ok'
#}
