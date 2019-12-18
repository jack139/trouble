#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

# 后台界面公用变量及函数

import web
import time, datetime, os
import urllib2
import re
from config import setting
#from app_helper import IS_TEST, CATEGORY

db = setting.db_web

web_session = None

ISOTIMEFORMAT=['%Y-%m-%d %X', '%Y-%m-%d', '%Y%m%d']

reg_b = re.compile(r"(android|bb\\d+|meego).+mobile|avantgo|bada\\/|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od)|iris|kindle|lge |maemo|midp|mmp|netfront|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)\\/|plucker|pocket|psp|series(4|6)0|symbian|treo|up\\.(browser|link)|vodafone|wap|windows (ce|phone)|xda|xiino", re.I|re.M)
reg_v = re.compile(r"1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\\-(n|u)|c55\\/|capi|ccwa|cdm\\-|cell|chtm|cldc|cmd\\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\\-s|devi|dica|dmob|do(c|p)o|ds(12|\\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\\-|_)|g1 u|g560|gene|gf\\-5|g\\-mo|go(\\.w|od)|gr(ad|un)|haie|hcit|hd\\-(m|p|t)|hei\\-|hi(pt|ta)|hp( i|ip)|hs\\-c|ht(c(\\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\\-(20|go|ma)|i230|iac( |\\-|\\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\\/)|klon|kpt |kwc\\-|kyo(c|k)|le(no|xi)|lg( g|\\/(k|l|u)|50|54|\\-[a-w])|libw|lynx|m1\\-w|m3ga|m50\\/|ma(te|ui|xo)|mc(01|21|ca)|m\\-cr|me(rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\\-2|po(ck|rt|se)|prox|psio|pt\\-g|qa\\-a|qc(07|12|21|32|60|\\-[2-7]|i\\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\\-|oo|p\\-)|sdk\\/|se(c(\\-|0|1)|47|mc|nd|ri)|sgh\\-|shar|sie(\\-|m)|sk\\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\\-|v\\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\\-|tdg\\-|tel(i|m)|tim\\-|t\\-mo|to(pl|sh)|ts(70|m\\-|m3|m5)|tx\\-9|up(\\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|yas\\-|your|zeto|zte\\-", re.I|re.M)

def time_str(t=None, format=0):
    return time.strftime(ISOTIMEFORMAT[format], time.localtime(t))

def detect_mobile():
    if web.ctx.has_key('environ') and web.ctx.environ.has_key('HTTP_USER_AGENT'):
        user_agent = web.ctx.environ['HTTP_USER_AGENT']
        b = reg_b.search(user_agent)
        v = reg_v.search(user_agent[0:4])
        if b or v:
            return True
    return False

def validateEmail(email):
    if len(email) > 7:
        if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) != None:
            return 1
    return 0

##############################################

# 用户等级
PRIV_USER     = 0b01000000  # 64
PRIV_DELIVERY = 0b00010000  # 16 # 要保留，区别后台用户与配送员
PRIV_ADMIN    = 0b00001000  # 8
PRIV_WX       = 0b00000100  # 4
PRIV_VISITOR  = 0b00000000  # 0

# 菜单权限
MENU_LEVEL = {
    'TICKET_OP'   : 0, # 问题处理
    'TICKET_USER' : 1, # 问题提交 
    'REPORT'      : 2, # 报表
    'ONDUTY'      : 3, # 值班记录
    'DHCDUTY'     : 4, # 东华值班记录
    'DIRCTOR'     : 5, # 主任审核
}

user_level = {
    PRIV_VISITOR  : '访客',
    PRIV_ADMIN    : '管理员',
    PRIV_USER     : '平台管理', 
}

#################

TICKET_TYPE = {
    100 : "HIS（门诊）",
    101 : "HIS（医生站）",
    102 : "HIS（护士站）",
    103 : "HIS（收费处）",
    200 : "HRP（财务）",
    201 : "HRP（人力）",
    202 : "HRP（物资）",
    300 : "PACS",
    400 : "LIS",
    500 : "支付平台",
    600 : "公众号",
    700 : "办公PC",
    800 : "打印机",
    900 : "网络",
    1000 : "电话",
    1100 : "自助机",
    90000 : "其他问题",
}

TICKET_SOURCE = {
    10 : "书面单据",
    20 : "值班",
    30 : "电话",
    40 : "微信",
    50 : "其他",
}

TICKET_STATUS = {
    #'WAIT'     : '等待处理',
    'OPEN'     : '处理中',
    #'PREOPEN'  : '等待重新处理',
    'PRECLOSE' : '等待确认完成',
    'CLOSED'   : '已完成',
    'NOGO'     : '无法解决',
}

# 关闭原因原因
_CLOSE_REASON = {
    '处理完成'       : 'A',
    '问题描述不清'    : 'B',
    '未发现问题'      : 'C',
    '提交了重复的问题' :'D',
}

# 对字典按照value排序
CLOSE_REASON = sorted(_CLOSE_REASON.iteritems(), key=lambda d: d[1])


# 为子文件传递session ---------------------

def set_session(s):
    global web_session
    web_session = s

def get_session_uname():
    return web_session.uname

#----------------------------------------

is_mobi=''  # '' - 普通请求，'M' - html5请求

def get_privilege_name(privilege=None, menu_level=None):
    if privilege==None:
        privilege = web_session.privilege

    name = ['?']
    p = int(privilege)
    if p==PRIV_ADMIN:
        return user_level[PRIV_ADMIN]
    if p&(PRIV_USER|PRIV_DELIVERY):
        if menu_level==None:
            menu_level = web_session.menu_level  # '----X--X----XXX---'
        for k in MENU_LEVEL.keys():
            if menu_level[MENU_LEVEL[k]]=='X':
                name.append(k)
    return name

def my_rand(n=5):
    import random
    return ''.join([random.choice('abcdefghijklmnopqrstuvwxyz') for ch in range(n)])

def logged(privilege = -1, menu_level=None):
    if web_session.login==1:
        if privilege == -1:  # 只检查login, 不检查权限
            return True
        else:
            if int(web_session.privilege) & privilege: # 检查特定权限
                if menu_level:
                    # 检查菜单权限
                    if web_session.menu_level[MENU_LEVEL[menu_level]]=='X':
                        return True
                    else:
                        return False
                else:
                    return True
            else:
                return False
    else:
        return False

def create_render(plain=False, globals={}, force_visitor=False):
    global is_mobi
    # check mobile
    if detect_mobile():
        is_mobi='M'
    else:
        is_mobi=''

    #print 'is_mobi', is_mobi

    if plain: layout=None
    else: layout='layout'

    privilege = web_session.privilege

    # 强制使用visitor模板
    if force_visitor:
        return web.template.render('templates/visitor', base=layout, globals=globals)

    if logged():
        if privilege == PRIV_WX:
            render = web.template.render('templates/wx', base=layout, globals=globals)
        elif privilege == PRIV_ADMIN:
            render = web.template.render('templates/admin', base=layout, globals=globals)
        elif privilege&PRIV_DELIVERY:
            print 'delivery'
            render = web.template.render('templates/user%s' % is_mobi, base=layout, globals=globals)
        elif privilege&PRIV_USER:
            print 'user'
            render = web.template.render('templates/user', base=layout, globals=globals)
        else:
            render = web.template.render('templates/visitor%s' % is_mobi, base=layout, globals=globals)
    else:
        render = web.template.render('templates/visitor%s' % is_mobi, base=layout, globals=globals)

    # to find memory leak
    #_unreachable = gc.collect()
    #print 'Unreachable object: %d' % _unreachable
    #print 'Garbage object num: %s' % str(gc.garbage)

    return render

