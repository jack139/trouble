基础表
base_image  图片
log_sys     后台操作日志
log_app     前台操作日志


功能表
user    后台登陆用户（系统）
app_user    前端用户（微信／app）


duty 值班记录
{
	duty_date	值班日期
	duty_uid		值班人uid
	room1_device	大机房设备状况 	0 正常 1 异常
	room2_device	小机房设备状况
	room1_ups		大机房ups
	room2_ups		小机房ups
	room1_conditioner	大机房空调
	room2_conditioner	小机房空调
	room1_temp_humi1	大机房温度/湿度1	{ temp: '', humi: '' }
	room1_temp_humi2	大机房温度/湿度2	
	room2_temp_humi		小机房温度/湿度
	device_issue		设备异常描述
	device_solution		设备解决办法

	system_big_issue	系统是否有重大事件 0 无 1 有
	system_issue 		系统异常描述
	system_solution		系统解决方法

	duty_log		值班工作记录

	status_key		钥匙交接情况 1 已交接 0 未交接
	status_phone	手机交接情况 1 已交接 0 未交接
	next_uid		交接人uid
	status_duty		值班记录状态： SAVED 未提交，未交接 CLOSED 已提交，未交接确认 FINISHED 已提交，已交接确认

	status_dhc		东华值班记录状态： SAVED 未提交，未交接 CLOSED 已提交，未交接确认 FINISHED 已提交，已交接确认

	save_t		保存时间
	close_t	    提交时间
	finish_t	交接时间
}

ticket 问题记录
{

}



/* -------------- Indexes ---------------*/

/* 后台建索引 db.collection.createIndex( { a: 1 }, { background: true } ) */

db.user.createIndex({privilege:1},{ background: true })
db.user.createIndex({uname:1},{ background: true })
db.user.createIndex({login:1, privilege:1},{ background: true })

db.sessions.createIndex({session_id:1},{ background: true })

db.app_sessions.createIndex({session_id:1},{ background: true })
db.app_sessions.createIndex({attime:1},{ background: true })
db.app_sessions.createIndex({type:1,attime:1},{ background: true })
db.app_sessions.createIndex({login:1,attime:1},{ background: true })
db.app_sessions.createIndex({uname:1},{ background: true })

db.app_user.createIndex({uname:1},{ background: true })
db.app_user.createIndex({app_id:1},{ background: true })
db.app_user.createIndex({openid:1},{ background: true })
db.app_user.createIndex({last_status:1},{ background: true })
db.app_user.createIndex({reg_time:1},{ background: true })

db.wx_user.createIndex({wx_user:1},{ background: true })
db.wx_user.createIndex({last_tick:1},{ background: true })

db.duty.createIndex({duty_date:1},{ background: true })

