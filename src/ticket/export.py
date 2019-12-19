#!/usr/bin/env python
# -*- coding: utf-8 -*-

import web
from openpyxl import Workbook
from tempfile import NamedTemporaryFile
import html2text
from config import setting
import helper

db = setting.db_web

PAGE_SIZE = 25

url = ('/ticket/export')

# - 导出报信息列表为 xlsx －－－－－－－－－－－

class handler:      
    def GET(self):
        if not helper.logged(helper.PRIV_USER,'TICKET_OP'):
            raise web.seeother('/')

        render = helper.create_render()
        user_data=web.input(name='', search_title='', search_type='', search_status='', search_uid='')

        # 取数据
        conditions ={}

        search_name = user_data.search_title.strip()
        if search_name!='':
            if search_name[0]=='#' and search_name[1:].isdigit():
                conditions['ticket_no'] = int(search_name[1:])
            else:
                conditions['title'] = { '$regex' : u'%s.*'%(search_name.replace('*','\\*').replace('?','\\?')), '$options' : 'i' }

        search_type = user_data.search_type.strip()
        if search_type!='':
            conditions['category'] = int(search_type)

        search_status = user_data.search_status.strip()
        if search_status!='':
            conditions['status'] = search_status

        search_uid = user_data.search_uid.strip()
        if search_uid!='':
            conditions['killer_uid'] = search_uid

        # 用户列表, 及东华用户列表
        user_list = {}
        db_user=db.user.find({})
        for u in db_user:
            if u['login']==0:
                continue
            if 'TICKET_OP' in helper.get_privilege_name(u['privilege'], u['menu_level']):
                user_list[u['uname']] = u['full_name']

        # 获取数据 （不分页）
        db_sku = db.ticket.find(conditions,
            sort=[('last_follow_tick', -1), ('last_tick', -1)]
        )

        # 转 xlsx
        wb = Workbook()
        gen_data(wb, db_sku, user_list)

        with NamedTemporaryFile() as tmp:
            wb.save(tmp.name)
            tmp.seek(0)
            stream = tmp.read()

        #web.header('Content-Type', 'text/plain; charset=utf-8')
        web.header('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        web.header("Content-Description", "File Transfer")
        web.header('Content-Disposition', 'attachment; filename="export.xlsx"')
        web.header("Content-Transfer-Encoding", "binary")
        web.header("Content-Length", "%d" % len(stream))
        web.header("Cache-Control", "must-revalidate")
        web.header("Pragma", "public")

        print 'stream: ', len(stream)

        return stream



TITLE = [
    '问题编号',
    '标题',
    '问题类型',
    '问题来源',
    '状态',
    '填报人',
    '处理人',
    '提交人/科室',
    '厂商对接人',
    '计划完成日期',
    '首次提交时间',
    '最后处理时间',
    '问题描述',
]

def gen_data(wb, r1, user_list):

    ws = wb.active

    data1 = []

    count = 0

    for x in r1:      
        detail_html = x.get('detail','')
        detail_text = html2text.html2text(detail_html)

        #print detail_text.encode('utf-8')

        data1.append([
            x['ticket_no'], # 问题编号
            x['title'], # 标题
            helper.TICKET_TYPE[x['category']] if x['category'] in helper.TICKET_TYPE.keys() else x['category'], #'* 问题类型',
            helper.TICKET_SOURCE[x['source']] if x['source'] in helper.TICKET_SOURCE.keys() else x['source'], #'* 问题来源',
            helper.TICKET_STATUS[x['status']] if x['status'] in helper.TICKET_STATUS.keys() else x['status'], #'* 状态',
            user_list[x.get('open_uid')], #'* 填报人',
            user_list[x.get('killer_uid')], #'* 处理人',
            x.get('submitter'), # '* 提交人/科室',
            x.get('vendor'), # '* 厂商对接人',
            x.get('plan_date'), # '* 计划完成日期
            x.get('first_date'), # '首次提交时间',
            x.get('last_date'), # '最后处理时间',
            detail_text, # '* 问题描述',
        ])

        count += 1

    ws.append(TITLE)
    for x in data1:
        try:
            ws.append(x)
        except:
            print x

