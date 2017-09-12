# coding=utf-8

import sys

import MySQLdb
import pandas as pd

reload(sys)
sys.setdefaultencoding("utf-8")

db = MySQLdb.connect("localhost", "root", "123456", "weibo_crawler")
db.set_character_set('utf8mb4')

cursor = db.cursor()

cursor.execute("SELECT VERSION()")
data = cursor.fetchone()
print "Database version: %s" %data

cursor.execute("DROP TABLE IF EXISTS weibo_data")

sql = "CREATE TABLE weibo_data(\
        cnt INT,\
        time VARCHAR(40),\
        weibo_from VARCHAR(80),\
        weibo_group VARCHAR(60),\
        repost_info VARCHAR(100),\
        content VARCHAR(2000),\
        attitude INT,\
        repost INT,\
        comment INT\
        )"

try:
    cursor.execute(sql)
    db.commit()
except:
    db.rollback()

df = pd.read_csv('output file/ssssygi/ssssygi.csv')
print len(df)

row = df.loc[0]
print row['cnt']

sql = "INSERT INTO weibo_data values(%f, %s, %s, %s, %s, %s, %d, %d, %d)"
tuple1 = tuple(row.tolist())

for index in range(len(df)):
    weibo_series = df.loc[index]
    weibo_list = weibo_series.tolist()
    print weibo_list[0]
    cursor.execute("INSERT INTO weibo_data VALUES (%d, '%s', '%s', '%s', '%s', '%s', %d, %d, %d)" \
        % (weibo_list[0],\
        weibo_list[1],\
        weibo_list[2],\
        weibo_list[3],\
        weibo_list[4],\
        weibo_list[5],\
        weibo_list[6],\
        weibo_list[7],\
        weibo_list[8]))
#cursor.execute(sql, tuple1)
db.commit()


db.close()
