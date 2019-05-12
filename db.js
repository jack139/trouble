基础表
base_image  图片
log_sys     后台操作日志
log_app     前台操作日志


功能表
user    后台登陆用户（系统）
app_user    前端用户（微信／app）






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

db.signup_user.createIndex({conf_id:1,completed:1},{ background: true })
db.signup_user.createIndex({openid:1},{ background: true })
db.signup_user.createIndex({name:1,phone:1,completed:1},{ background: true })

db.job_sheet.createIndex({xm:1},{ background: true })
db.job_sheet.createIndex({submit_time:1},{ background: true })
