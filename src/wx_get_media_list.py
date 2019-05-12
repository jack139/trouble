#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2, urllib
import json
#from config import setting

# 
wx_appid=''
wx_secret='9e9ee82b0f6083311ec1c51e726dedf0'

wx_param={
    "type"   : "news",
    "offset" : 0,
    "count"  : 20,
}

def get_token():
    url='https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s' % \
        (wx_appid, wx_secret)
    f=urllib.urlopen(url)
    data = f.read()
    f.close()

    t=json.loads(data)
    if t.has_key('access_token'):
        return t['access_token']
    else:
        return ''

def get_media_list(access_token):
    t=json.dumps(wx_param, ensure_ascii=False)
    f = urllib2.urlopen(
        url = 'https://api.weixin.qq.com/cgi-bin/material/batchget_material?access_token=%s' % access_token,
        data    = t
        )
    ret=f.read()
    #print ret

    r2 = json.loads(ret)
    for i in r2['item']:
        print i['media_id']
        for j in i['content']['news_item']:
            print j['title']


if __name__ == '__main__':
    my_token=get_token()
    #my_token='cI4OABcORaGjqdXhQmfGLbPv0CHgSxQpQmUsAJeNyLhe8Fy5i_L6NcB6bTze59QXvbXoMcKQXsV9Lo6TLCScYA'
    print my_token

    get_media_list(my_token)

