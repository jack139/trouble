#!/usr/bin/env python
# -*- coding: utf-8 -*-
import web
from pymongo import MongoClient

#####
debug_mode = True   # Flase - production, True - staging
#####
#
enable_proxy = True
http_proxy = 'http://192.168.2.108:8888'
https_proxy = 'https://192.168.2.108:8888'
proxy_list = ['192.168.2.103']
enable_local_test = True
#####

db_serv_list='127.0.0.1'
# db_serv_list='mongodb://10.168.11.151:27017,10.252.95.145:27017,10.252.171.8:27017/?replicaSet=rs0'

cli = {
    'web'  : MongoClient(db_serv_list),
}
# MongoClient('10.168.11.151', replicaset='rs0', readPreference='secondaryPreferred') # 使用secondary 读
# MongoClient('mongodb://10.168.11.151:27017,10.252.95.145:27017,10.252.171.8:27017/?replicaSet=rs0')

db_web = cli['web']['trouble_db']
db_web.authenticate('ipcam','ipcam')

db_primary = db_web

thread_num = 1
auth_user = ['test','gt']
cs_admin = ['cs0']

tmp_path = '/usr/local/nginx/html/xah/static/tmp'
logs_path = '/usr/local/nginx/logs'
image_store_path = '/usr/share/nginx/html/xah/static/upload'

app_host='xah-wx.xmu.edu.cn'
wx_host='xah-wx.xmu.edu.cn'
image_host='xah-wx.xmu.edu.cn/static'
notify_host='xah-wx.xmu.edu.cn'
app_pool=['xah-wx.xmu.edu.cn']

WX_store = {
    '000' : { # 测试
        'wx_appid' : '',
        'wx_appsecret' : '9e9ee82b0f6083311ec1c51e726dedf0',
        'mch_id' : '1408035102',
    },

}


# 微信设置
region_id = '000'
wx_setting = WX_store[region_id]

order_fuffix=''

http_port=8000
https_port=443

mail_server='127.0.0.1'
sender='"jack139"<jack139@gmail.com>'
worker=['jack139@gmail.com']

web.config.debug = debug_mode

config = web.storage(
    email = 'jack139@gmail.com',
    site_name = 'ipcam',
    site_des = '',
    static = '/static'
)
