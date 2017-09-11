# coding=utf-8
import sys
import traceback

import MySQLdb

reload(sys)
sys.setdefaultencoding("utf-8")


# Create seed user table
def create_seed_user_table(table_name):
    db = MySQLdb.connect("localhost", "root", "123456", "weibo_crawler")
    cursor = db.cursor()
    sql = "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES where TABLE_SCHEMA = 'weibo_crawler' and TABLE_NAME = '%s'" % table_name
    cursor.execute(sql)
    result = cursor.fetchall()
    if result:
        print 'Warning: Table \'%s\' already exists' % table_name
    else:
        sql = 'CREATE TABLE %s(\
                id INT NOT NULL AUTO_INCREMENT,\
                user_id VARCHAR(30),\
                update_time VARCHAR(40),\
                PRIMARY KEY (id)\
                )' % table_name
        try:
            cursor.execute(sql)
            db.commit()
            print 'Create table \'%s\' succeed' % table_name
        except Exception, e:
            print 'Error occurs while creating table \'%s\'' % table_name
            traceback.print_exc()
            print traceback.format_exc()
    db.close()

# Insert seed user data
def insert_user_to_seed_table(table_name, user_id):
    db = MySQLdb.connect("localhost", "root", "123456", "weibo_crawler")
    cursor = db.cursor()
    sql = "SELECT * FROM %s where user_id = \'%s\'" % (table_name, user_id)
    cursor.execute(sql)
    result = cursor.fetchall()
    if result:
        print 'User %s already exists in table %s' % (user_id, table_name)
    else:
        sql = "INSERT INTO %s(user_id) VALUES (\'%s\')" % (table_name, user_id)
        cursor.execute(sql)
        db.commit()
    db.close()


'''
sql = "SELECT uid FROM seed_user"

try:
    cursor.execute(sql)
    result = cursor.fetchall()
    for uid in result:
        print uid
except:
    print "Error: unable to fetch data"
'''
if __name__ == '__main__':
    #create_seed_user_table('seed_user')
    insert_user_to_seed_table('seed_user', '12345')
