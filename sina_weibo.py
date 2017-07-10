# coding=utf-8

import sys

from content_parsing_tool import *

reload(sys)
sys.setdefaultencoding("utf-8")

class sina_weibo():
    def __init__(self, user_id, base_url, home_page):
        self.user_id = user_id
        self.base_url = base_url
        self.home_page = home_page
        self.basic_info = get_basic_info(self.home_page)
        self.weibo_content = dict()

    def display_basic_info(self):
        print '\n\n----------------------------------------\n'
        print '昵称：' + self.basic_info['username'] + '    ',
        print self.basic_info['sex'] + '/' + self.basic_info['region'] + '\n'
        print self.basic_info['weibo_num'] + '  |  ',
        print self.basic_info['follow'] + '  |  ',
        print self.basic_info['fans'] + '\n'
        print '简介：' + self.basic_info['signature']
        print '\n共有微博内容%d页' % (int(self.basic_info['page_num']))
        print '\n----------------------------------------\n\n'

