#!/usr/bin/python3
# 获取地区编号和名称
import pymysql
import pdb
from config import user, passwd, the_db

db = pymysql.connect(host="localhost", port=3306, user=user,
                     passwd=passwd, db=the_db, charset="utf8")
# pdb.set_trace()
cursor = db.cursor()
f = open('weather_id.txt')
for line in f:
    linelist = line.rstrip().split("=")
    print(linelist)
    sql = "insert into weather(Weather_id,name) values('%s','%s')" % (linelist[0], linelist[1])
    cursor.execute(sql)
    db.commit()
db.close()
