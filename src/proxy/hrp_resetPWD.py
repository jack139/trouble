#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
import web
import time, hashlib, json
from suds.client import Client

# 交接记录

url = ('/proxy/hrp/resetpwd')


def generate_sign(c): # c是列表
    PRIVATE_KEY = 'a6ec0a4821c9'
    #验证签名
    sign_str = '%s%s' % (PRIVATE_KEY, ''.join(i for i in c))
    #print sign_str.encode('utf-8')
    return hashlib.md5(sign_str.encode('utf-8')).hexdigest().upper()

class handler:
    def POST(self):
        web.header('Content-Type', 'application/json')
        param = web.input(authcode='',clerkcode='',oldpwd='',newpwd='')

        print param

        authcode = generate_sign([param.clerkcode, param.oldpwd, param.newpwd])

        print authcode

        if authcode!=param.authcode:
            return json.dumps({'ret' : -9, 'data' : 'auth fail' })

        wsdl_url = 'http://172.27.70.26:8099/uapws/service/otherHrp?wsdl'
        headers={'Content-Type':'application/soap+xml;charset="UTF-8"'}
        client=Client(wsdl_url,headers=headers,faults=False,timeout=15)

        requestPara = '{"orgcode":"10","clerkcode":"%s","oldpwd":"%s","newpwd":"%s","comfirmpwd":"%s"}' % \
            (param.clerkcode, param.oldpwd, param.newpwd, param.newpwd)

        result=client.service.resetPWD(requestPara)

        result1 = json.loads(result[1])

        # 返回
        if result1['errcode']=="0":
            return json.dumps({'ret' : 0, 'data' : "ok" })    
        else:
            return json.dumps({'ret' : -1, 'data' : result1['errmsg'] })
