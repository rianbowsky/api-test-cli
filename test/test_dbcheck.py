import init

from core.mysql_check import MysqlCheck


# 入参
sql = 'select * from bs_users where id={id}'
args = {'id':'$resp.data.uid'}
wants = {
    "id": ["=", '$resp.data.uid'],
    "phone": "$param.phone"
}
context = {
    "param": {
        "phone": "18681636749"
    },
    "resp": {
            "data": {
            "uid": 2
        },
        "errCode": 0
    }
}

from pymysql import connect
from _conf_db import mysqlConf as conf
db= connect(
    host= conf['host'],
    port= conf['port'],
    user= conf['user'],
    passwd= conf['passwd'],
    db= conf['db']
)
v = MysqlCheck(db, sql, args, wants)
ok = v.check(context)
print(ok, v.logg())
