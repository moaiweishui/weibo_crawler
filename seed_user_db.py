# coding=utf-8

import MySQLdb

db = MySQLdb.connect("localhost", "root", "123456", "weibo_crawler")

cursor = db.cursor()

sql = "SELECT uid FROM seed_user"

try:
    cursor.execute(sql)
    result = cursor.fetchall()
    for uid in result:
        print uid
except:
    print "Error: unable to fetch data"

db.close()
