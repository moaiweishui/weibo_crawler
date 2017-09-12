# coding=utf-8
import sys
import traceback

import MySQLdb

reload(sys)
sys.setdefaultencoding("utf-8")


def create_user_info_table(table_name='user_info', is_drop_old_table=False):
    db = MySQLdb.connect("localhost", "root", "123456", "weibo_crawler")
    db.set_character_set('utf8mb4')
    cursor = db.cursor()
    if is_drop_old_table:
        cursor.execute('DROP TABLE IF EXISTS %s' % table_name)
        db.commit()
    sql = "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = 'weibo_crawler' AND TABLE_NAME = '%s'" % table_name
    cursor.execute(sql)
    result = cursor.fetchall()
    if result:
        print 'Warning: Table %s already exists' % table_name
        db.close()
    else:
        sql = 'CREATE TABLE %s(\
                id int NOT NULL AUTO_INCREMENT,\
                user_id VARCHAR(30) NOT NULL,\
                username VARCHAR(40),\
                sex VARCHAR(10),\
                region VARCHAR(30),\
                signature VARCHAR(200),\
                weibo_num VARCHAR(20),\
                follow VARCHAR(20),\
                fans VARCHAR(20),\
                PRIMARY KEY(id)\
                )' % table_name
        try:
            cursor.execute(sql)
            db.commit()
            print "Create table '%s' succeed" % table_name
        except Exception, e:
            db.rollback()
            print 'Error occurs while creating table \'%s\'' % table_name
            traceback.print_exc()
            print traceback.format_exc()
        finally:
            db.close()


def is_user_info_exists(user_id, table_name='user_info'):
    db = MySQLdb.connect("localhost", "root", "123456", "weibo_crawler")
    cursor = db.cursor()
    sql = "SELECT * FROM %s WHERE user_id = '%s'" % (table_name, user_id)
    cursor.execute(sql)
    result = cursor.fetchall()
    db.close()
    if result:
        return True
    else:
        return False


def insert_new_user(basic_info, table_name='user_info'):
    user_id = basic_info['user_id']
    if is_user_info_exists(user_id, table_name):
        print 'User %s info exists'
    else:
        db = MySQLdb.connect("localhost", "root", "123456", "weibo_crawler")
        db.set_character_set('utf8mb4')
        cursor = db.cursor()
        sql = "INSERT INTO %s (\
                user_id,\
                username,\
                sex,\
                region,\
                signature,\
                weibo_num,\
                follow,\
                fans)\
                VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')"\
                % (table_name, \
                basic_info['user_id'],\
                basic_info['username'],\
                basic_info['sex'],\
                basic_info['region'],\
                basic_info['signature'],\
                basic_info['weibo_num'],\
                basic_info['follow'],\
                basic_info['fans'],\
                )
        try:
            cursor.execute(sql)
            db.commit()
            print 'Insert user %s to table %s succeed' % (user_id, table_name)
        except Exception, e:
            db.rollback()
            print 'Error occurs while creating table \'%s\'' % table_name
            traceback.print_exc()
            print traceback.format_exc()
        finally:
            db.close()

if __name__ == '__main__':
    create_user_info_table('user_info')

