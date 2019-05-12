#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from openpyxl import Workbook
from config import setting
db = setting.db_web

TITLE1 = [
    '"baseinfo_$head,name,sex,idtype,id,birthdate,nationality,polity,country,nativeplace,mobile,email,glbdef1,glbdef2,glbdef3,glbdef4,glbdef5,glbdef6,glbdef7,glbdef8,glbdef9,glbdef10,glbdef11,glbdef12,glbdef13,glbdef14,glbdef15,glbdef16,glbdef17,glbdef18,glbdef19,glbdef20,frolanlevel,joinworkdate,permanreside,characterrpr,health,marital,marriagedate,glbdef21,glbdef23,evaluation,personal,glbdef25,glbdef26,glbdef27,glbdef29,glbdef30,glbdef28,glbdef22,workunitnow,remark"', 
    '* 姓名(ZH)',   
    '性别',
    '* 证件类型',
    '* 证件号码',
    '* 出生日期',
    '* 民族',
    '* 政治面貌',
    '* 国籍/地',
    '* 籍贯',
    '* 联系电话',
    '* 联系邮箱',
    '现任党政管理职务',
    '现任党政管理职务时间',
    '* 现工作医院等级',
    '* 三甲医院工作时间（年）',
    '学术兼职',
    '* 研究生导师资格',
    '* 导师资格聘任时间',
    '* 现专业技术资格',
    '* 现专业技术资格取得日期',
    '* 现专业技术资格专业名称',
    '专技职务/行政等级',
    '现受聘专业技术职务',
    '现专业技术职务聘任时',
    '现专业技术职务聘任专业名称',
    '执业类别',
    '执业范围',
    '现教师系列专业技术职务所聘学',
    '现教师系列专业技术职',
    '现教师系列专业技术职务任职时',
    '* 身高（cm）',
    '* 英语水平',
    '* 参加工作日期',
    '* 户口所在',
    '* 户口性质',
    '* 健康状况',
    '* 婚姻状况',
    '* 结离(婚)日期',
    '* 生育子女',
    '年龄',
    '科研项目',
    '科研成果',
    '获奖情况',
    '参与科研项目情况（项目合同书中有署名的才算参与）',
    '论文论著情况',
    '参加学术团体及任职情况',
    '临床主要业绩',
    '其他成果',
    '* 人员类别',
    '现工作单位',
    '备注',
]    

TITLE2 = [
    '"rm_psndoc_job,pk_reg_org,pk_reg_dept,pk_reg_job,pk_reg_job.jobtype_301,pk_reg_job.majortype_301,reg_date"',
    '* 应聘组织',
    '应聘部门',
    '* 应聘职位',
    '岗位类别',
    '专业类别',
    '应聘日期',
]

TITLE3 = [
    '"rm_psndoc_edu,education,begindate,enddate,school,major,degree,degreedate,glbdef1,studymode,glbdef2,lastflag,remark"',
    '学历',
    '入学日期',
    '毕业日期',
    '* 学校',
    '专业',
    '学位',
    '学位授予日期',
    '学位国家',
    '学习方式',
    '培养类型',
    '是否最高学历',
    '备注',
]

TITLE4 = [
    '"rm_psndoc_family,mem_name,mem_relation,mem_corp,mem_job,glbdef1,glbdef2,vrelaaddr,vrelaphone,remark"',
    '* 家庭成员姓名',
    '* 与本人关系',
    '工作单位',
    '职务',
    '配偶最高学历',
    '配偶最高学位',
    '联系地址',
    '联系电话',
    '备注',
]

TITLE5 = [
    '"rm_psndoc_work,begindate,enddate,workcorp,glbdef1,workdept,workjob,remark"',
    '* 开始日期',
    '结束日期',
    '* 工作单位',
    '医院等级',
    '所在部门',
    '担任职务',
    '备注',
]

TITLE6 = [
    '"rm_psndoc1,glbdef1,glbdef2,glbdef3,glbdef4,glbdef5,glbdef6,glbdef7"',
    '规培情况说明',
    '规培单位',
    '规培起始时间',
    '规培结束时间',
    '培训专业',
    '是否合格',
    '规培证取得日期',
]



def gen_data(wb, begin_date, end_date):
    ws = wb.active

    ws['A1'] =  '*导入须知:\r\n' \
        '1.表格中不能增、删、改列及固有内容\r\n' \
        '2.所有内容必须为文本格式;表格中有多个档案名称字段是为了实现多语,如果没有多语只录第一个名称字段即可\r\n' \
        '3.枚举项输入错误时，则按默认值处理;勾选框的导入需输入N、Y\r\n' \
        '4.导入带有子表的档案时,表格中主表与子表之间必须有一空行,且主、子表对应数据需加上相同的行号' 

    condition = {
        '$and' : [ {'submit_time' : {'$gt' : begin_date}},
                   {'submit_time' : {'$lt' : end_date  }} ],
    }

    data1 = []
    data2 = []
    data3 = []
    data4 = []
    data5 = []
    data6 = []

    count = 0

    r1 = db.job_sheet.find(condition, sort=[('submit_time', -1)])
    for x in r1:
        
        data1.append([
            count, 
            x['xm'], # 姓名
            #x['xm'][0], # 姓
            #x['xm'][1:], # 名
            1 if x['xb']==u'男' else 2, # 性别
            x['zjlx'], # 证件类型
            x['zjhm'], #'* 证件号码',
            x['csrq'], #'* 出生日期',
            x['mz'], #'* 民族',
            x['zzmm'][1] if len(x['zzmm'])>1 else '', #'* 政治面貌',
            x['gjdq'][1] if len(x['gjdq'])>1 else '', #'* 国籍/地',
            x['jg_code'], #'* 籍贯',
            x['lxdh'], # '* 联系电话',
            x['lxyx'], # '* 联系邮箱',
            x['dzglzw'], # '现任党政管理职务',
            x['dzglsj'], # '现任党政管理职务时间',
            x['gzyydj'], # '* 现工作医院等级',
            x['sjyygzsj'], # '* 三甲医院工作时间（年）',
            x['xsjz'], # '学术兼职' 
            x['yjsdszg'], # '* 研究生导师资格',
            x['dszgprsj'], # '* 导师资格聘任时间',
            x['zyjszg'][1] if len(x['zyjszg'])>1 else '', # '* 现专业技术资格',
            x['zyjszgqdsj'], # '* 现专业技术资格取得日期',
            x['zyjszgzymc'], # '* 现专业技术资格专业名称',
            x['xzdj'], # '专技职务/行政等级',
            x['xspzyjszw'][1] if len(x['xspzyjszw'])>1 else '', # '现受聘专业技术职务',
            x['xzyjszwprsj'], # '现专业技术职务聘任时',
            x['xzyjszwprmc'], # '现专业技术职务聘任专业名称',
            x['zhiylb'], # '执业类别',
            x['zhiyfw'], # '执业范围',
            x['jsxlzyjsxx'], # '现教师系列专业技术职务所聘学',
            x['jsxlzyjszw'], # '现教师系列专业技术职',
            x['jsxlzyjsrzsj'], # '现教师系列专业技术职务任职时',
            x['sglm'], # '* 身高（cm）',
            x['yysp'], # '* 英语水平',
            x['cjgzrq'], # '* 参加工作日期',
            x.get('hjdz_code',''), #'* 户口所在',
            x['hjxz'], # '* 户口性质',
            x['jkzk'], # '* 健康状况',
            x['hyzk'], # '* 婚姻状况',
            x['jhrq'], # '* 结离(婚)日期',
            x['syzn'], # '* 生育子女',
            x['nl'], # '年龄',
            x['kyxm'], # '科研项目',
            x['cgjl'], # '科研成果',
            x.get('hjqk', ''), # 获奖情况 #2019-01-18
            x.get('cykyxmqk', ''), # 参与科研项目情况 #2019-01-18
            x.get('lwlzqk', ''), # 论文论著情况 #2019-01-18
            x.get('xsttrzqk', ''), # 参加学术团体及任职情况 #2019-01-18
            x.get('lczyyj', ''), # 临床主要业绩 #2019-01-18
            x.get('qtcg', ''), # 其他成果 #2019-01-18
            x['rylb'], # '* 人员类别',
            x['xgzdw'], # '现工作单位',
            x['qtbz'], # '备注',
        ])

        data2.append([
            count,
            '厦门大学附属翔安医院', # '* 应聘组织',
            x['sbgw'][1], # '应聘部门',
            x['sbgw'][2], # '* 应聘职位',
            x['gwlb'], # '岗位类别',
            x['zylb'], # '专业类别',
            x['submit_time'][:10], # 应聘日期
        ])

        for i in x['study_list']:
            if i['byxx'].strip()!='': # 过滤掉毕业学校为空的项目 2018-10-29
                data3.append([
                    count,
                    i['xl'][1] if len(i['xl'])>1 else '', #'学历',
                    i['rxsj']+'-01' if len(i['rxsj'])>0 else i['rxsj'], #'入学日期',
                    i['bysj']+'-01' if len(i['bysj'])>0 else i['bysj'], #'毕业日期',
                    i['byxx'], #'* 学校',
                    i['sxzy'], #'专业',
                    i['xw'][1] if len(i['xw'])>1 else '', #'学位',
                    i['xwsj'], #'学位授予日期',
                    i['xwgj'][1] if len(i['xwgj'])>1 else '', #'学位国家',
                    i['xxxs'][1] if len(i['xxxs'])>1 else '', #'学习方式',
                    i['pylx'], #'培养类型',
                    'Y' if i['zgxl']==u'是' else 'N', #'是否最高学历',
                    '', #'备注',
                ])


        if x['poxm'].strip()!='':
            pozgxl = x.get('pozgxl', '').split('|')
            pozgxw = x.get('pozgxw', '').split('|')
            data4.append([
                count,
                x['poxm'], # '* 家庭成员姓名',
                '配偶' if x['poxm'].strip()!='' else '', # '* 与本人关系',
                x['podw'], # '工作单位',
                x['pozw'], # '职务',
                pozgxl[1] if len(pozgxl)>1 else '', # '配偶最高学历', #2019-02-01
                pozgxw[1] if len(pozgxw)>1 else '', # '配偶最高学位', #2019-02-01
                '', # '联系地址',
                '', # '联系电话',
                '', # '备注',
            ])


        for i in x['job_list']:
            if i['kssj'].strip()!='' and i['gzdw'].strip()!='':
                data5.append([
                    count,
                    i['kssj'], # '* 开始日期',
                    i['jssj'], # '结束日期',
                    i['gzdw'], # '* 工作单位',
                    i['yydj'], # '医院等级',
                    i['szbm'], # '所在部门',
                    i['zyzw'], # '担任职务',
                    '', # '备注',
                ])


        data6.append([
            count,
            x['gpqk'], # '规培情况说明',
            x['gpdw'], # '规培单位',
            x['gpqssj'], # '规培起始时间',
            x['gpjssj'], # '规培结束时间',
            x['gpzy'], # '培训专业',
            x['gphg'], # '是否合格',
            x['gpzrq'], # '规培证取得日期',
        ])

        count += 1

    ws.append(TITLE1)
    for x in data1:
        ws.append(x)

    ws.append([''])

    ws.append(TITLE2)
    for x in data2:
        ws.append(x)

    ws.append([''])

    ws.append(TITLE3)
    for x in data3:
        ws.append(x)

    ws.append([''])

    ws.append(TITLE4)
    for x in data4:
        ws.append(x)

    ws.append([''])

    ws.append(TITLE5)
    for x in data5:
        ws.append(x)

    ws.append([''])

    ws.append(TITLE6)
    for x in data6:
        ws.append(x)

if __name__ == '__main__':
    if len(sys.argv)<3:
        print "usage: python %s <begin_date> <end_date>" % sys.argv[0]
        sys.exit(2)

    begin_date = '%s 00:00:00' % sys.argv[1]
    end_date = '%s 23:59:59' % sys.argv[2]

    wb = Workbook()
    gen_data(wb, begin_date, end_date)

    wb.save(sys.argv[1]+'_'+sys.argv[2]+'.xlsx')
