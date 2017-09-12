#coding=utf-8

import pandas as pd
from cassandra.cluster import Cluster

cluster = Cluster(['127.0.0.1'])
session = cluster.connect('myspace')

session.execute('USE myspace')
session.execute('DROP TABLE IF EXISTS weibo_data')
msg = session.execute('CREATE TABLE IF NOT EXISTS weibo_data(\
        id int,\
        cnt int,\
        time text,\
        weibo_from text,\
        weibo_group text,\
        repost_info text,\
        content text,\
        attitude int,\
        repost int,\
        comment int,\
        PRIMARY KEY((id, cnt), time)\
        )')

df = pd.read_csv('output file/ssssygi/ssssygi.csv')
print 'Data length:' + str(len(df))

row = df.loc[0]
print row['cnt']

cql = "INSERT INTO weibo_data values(%f, %s, %s, %s, %s, %s, %d, %d, %d)"
tuple1 = tuple(row.tolist())
weibo_id = 0
for index in range(len(df)):
    weibo_series = df.loc[index]
    weibo_list = weibo_series.tolist()
    #print weibo_list[8]
    cql = "INSERT INTO weibo_data (id,\
            cnt,\
            time,\
            weibo_from,\
            weibo_group,\
            repost_info,\
            content,\
            attitude,\
            repost,\
            comment)\
        VALUES (%d, %d, '%s', '%s', '%s', '%s', '%s', %d, %d, %d)"\
        % (weibo_id,\
        weibo_list[0],\
        weibo_list[1],\
        weibo_list[2],\
        weibo_list[3],\
        weibo_list[4],\
        weibo_list[5],\
        weibo_list[6],\
        weibo_list[7],\
        weibo_list[8])
    #print cql
    session.execute(cql)
    weibo_id += 1


