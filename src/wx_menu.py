#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2, urllib
import json
#from config import setting

wx_appid='wxf28f23539c5821be'
wx_secret='9e9ee82b0f6083311ec1c51e726dedf0'

wx_menu={
    'button':[
        {
            'name':'医院资讯',
            'sub_button':[
                {
                    'type':'view',
                    'name':'医院概况',
                    'url'  : 'http://mp.weixin.qq.com/s?__biz=MzUzMjYxNjg2OA==&mid=100000005&idx=1&sn=6eeb5d01a9d50b3d85751265f169cbc0&chksm=7ab1c2ce4dc64bd816e1935da3da633c7b58797c22d43f614380f01be6a67b993151ad38cd0b&scene=18#wechat_redirect',
                },
                {
                    'type' :'media_id',
                    'name' :'医院新闻',
                    'media_id'  : 'yv6zc-7W2WLqyZT8dQoUYGivOy3Vt_ndP3oMjyfwk5E',
                },
                #{
                #    'type':'click',
                #    'name':'通知公告',
                #    'key'  : 'CLICK_WAIT',
                #},
                {
                    'type':'media_id',
                    'name':'党建工作',
                    'media_id'  : 'yv6zc-7W2WLqyZT8dQoUYAUn3q6cBQSMXWiMz_c2pfo',
                },
                {
                    'type':'click',
                    'name':'医学人文',
                    'key'  : 'CLICK_WAIT',
                },
            ]
        },
        #{
        #    'name':'科室介绍',
        #    'sub_button':[
        #        {
        #            'type':'click',
        #            'name':'科室设置',
        #            'key'  : 'CLICK_WAIT',
        #        },
        #        {
        #            'type':'click',
        #            'name':'学科团队',
        #            'key'  : 'CLICK_WAIT',
        #        },
        #        {
        #            'type':'click',
        #            'name':'专家介绍',
        #            'key'  : 'CLICK_WAIT',
        #        },
        #    ]
        #},
        {
            'name' : '专家介绍',
            'type' : 'view',
            'url'  : 'http://xah.xmu.edu.cn/docList.jsp?urltype=tree.TreeTempUrl&wbtreeid=1050',
        },
        {
            'name':'就医导航',
            'sub_button':[
                #{
                #    'type':'view',
                #    'name':'内部测试',
                #    'url'  : 'http://xah-wx3.xmu.edu.cn:9090/hospitalPortal-web/xiamen/xianganyiyuan/index',
                #},
                {
                    'type':'click',
                    'name':'交通指南',
                    'key'  : 'CLICK_WAIT',
                },
                {
                    'type':'click',
                    'name':'门诊指南',
                    'key'  : 'CLICK_WAIT',
                },
                {
                    'type':'click',
                    'name':'预约挂号',
                    'key'  : 'CLICK_WAIT',
                },
                #{
                #    'type':'click',
                #    'name':'当日挂号',
                #    'key'  : 'CLICK_WAIT',
                #},
                #{
                #    'type':'click',
                #    'name':'医保政策',
                #    'key'  : 'CLICK_WAIT',
                #},
                #{
                #    'type':'view',
                #    'name':'报名测试',
                #    'url'  : 'http://xah-wx.xmu.edu.cn/wx/init_signup',
                #},
            ]
        },
        #{
        #    'name':'高峰论坛',
        #    'sub_button':[
        #        {
        #            'type':'view',
        #            'name':'论坛介绍',
        #            #'url' :'http://h.eqxiu.com/s/Rl0azfod',
        #            #'url' :'https://e.eqxiu.com/s/duBZfY9J',
        #            'url' :'https://i.eqxiu.com/s/mvguSpDW',
        #        },
        #        #{
        #        #    'type':'view',
        #        #    'name':'参会报名',
        #        #    'url' :'http://xah-wx.xmu.edu.cn/wx/init_signup',
        #        #},
        #        {
        #            'type':'view',
        #            'name':'会议通知文件',
        #            'url' :'http://mp.weixin.qq.com/s/5yCI9WD-LwNjcZTwoa8UVA',
        #            #'url' :'http://xah-wx.xmu.edu.cn/notice20180405.pdf',
        #            #'key'  : 'CLICK_PDF',
        #        },
        #    ]
        #},
    ]
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

def creat_menu(access_token):
    t=json.dumps(wx_menu, ensure_ascii=False)
    f = urllib.urlopen(
        url = 'https://api.weixin.qq.com/cgi-bin/menu/create?access_token=%s' % access_token,
        data = t
    )
    ret=f.read()
    print ret

if __name__ == '__main__':

    my_token=get_token()
    #my_token='cI4OABcORaGjqdXhQmfGLbPv0CHgSxQpQmUsAJeNyLhe8Fy5i_L6NcB6bTze59QXvbXoMcKQXsV9Lo6TLCScYA'
    print my_token

    creat_menu(my_token)

