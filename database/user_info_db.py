# coding=utf-8
import sys
import traceback

import MySQLdb

reload(sys)
sys.setdefaultencoding("utf-8")

db = MySQLdb.connect("localhost", "root", "123456", "weibo_crawler")
    cursor = db.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    try:
            cursor.execute(sql)
            db.commit()
            print 'Create table \'%s\' succeed' % table_name
        except Exception, e:
            db.rollback()
            print 'Error occurs while creating table \'%s\'' % table_name
            traceback.print_exc()
            print traceback.format_exc()
    db.close()
