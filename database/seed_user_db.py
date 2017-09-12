# coding=utf-8
import sys
import traceback

import MySQLdb

reload(sys)
sys.setdefaultencoding("utf-8")


# Create seed user table
def create_seed_user_table(table_name, is_drop_old_table=False):
    db = MySQLdb.connect("localhost", "root", "123456", "weibo_crawler")
    cursor = db.cursor()
    if is_drop_old_table:
        cursor.execute('DROP TABLE IF EXISTS %s' % table_name)
        db.commit()
    sql = "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES where TABLE_SCHEMA = 'weibo_crawler' and TABLE_NAME = '%s'" % table_name
    cursor.execute(sql)
    result = cursor.fetchall()
    if result:
        print 'Warning: Table \'%s\' already exists' % table_name
        db.close()
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
            db.rollback()
            print 'Error occurs while creating table \'%s\'' % table_name
            traceback.print_exc()
            print traceback.format_exc()
        finally:
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
        db.close()
    else:
        sql = "INSERT INTO %s(user_id) VALUES (\'%s\')" % (table_name, user_id)
        try:
            cursor.execute(sql)
            db.commit()
        except Exception, e:
            db.rollback()
            print 'Error occurs while inserting data'
            traceback.print_exc()
            print traceback.format_exc()
        finally:
            db.close()

# Update user in seed_user table
def update_user_in_seed_table(table_name, user_id, update_time):
    db = MySQLdb.connect("localhost", "root", "123456", "weibo_crawler")
    cursor = db.cursor()
    sql = "SELECT * FROM %s where user_id = \'%s\'" % (table_name, user_id)
    cursor.execute(sql)
    result = cursor.fetchall()
    if not result:
        print 'User %s does not exists in table %s' % (user_id, table_name)
        db.close()
    else:
        sql = "UPDATE %s SET update_time = \'%s\' WHERE user_id = \'%s\'" % (table_name, update_time, user_id)
        try:
            cursor.execute(sql)
            db.commit()
        except Exception, e:
            db.rollback()
            print 'Error occurs while updating data'
            traceback.print_exc()
            print traceback.format_exc()
        finally:
            db.close()

# Get seed user id
# only_new:  true: have not been crawled
#           false: all of the seed users
def get_seed_user(table_name, only_new=True):
    seed_user_list = []
    db = MySQLdb.connect("localhost", "root", "123456", "weibo_crawler")
    cursor = db.cursor()
    sql = "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES where TABLE_SCHEMA = 'weibo_crawler' and TABLE_NAME = '%s'" % table_name
    cursor.execute(sql)
    result = cursor.fetchall()
    if not result:
        print 'Table %s not exists' % table_name
        db.close()
    else:
        if only_new:
            sql = 'SELECT user_id FROM %s WHERE update_time IS NULL' % table_name
        else:
            sql = 'SELECT user_id FROM %s' % table_name
        try:
            cursor.execute(sql)
            rows = cursor.fetchall()
            for row in rows:
                seed_user_list.append(row[0])
            db.commit()

        except Exception, e:
            db.rollback()
            print 'Error occurs while updating data'
            traceback.print_exc()
            print traceback.format_exc()
        finally:
            db.close()
    return seed_user_list


if __name__ == '__main__':
    #create_seed_user_table('seed_user')
    #insert_user_to_seed_table('seed_user', '')
    #insert_user_to_seed_table('seed_user', '')
    #update_user_in_seed_table('seed_user', '12345', '2017-9-13')
    seed_user_list = get_seed_user('seed_user')
    for x in seed_user_list:
        print x
