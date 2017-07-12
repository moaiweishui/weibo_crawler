# -*- coding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from content_parsing_tool import *
from sina_weibo import *
from wap_weibo_crawler import *

DEBUG = False

if DEBUG:
    filename = raw_input('请输入文件名:\n')
    filename = 'output file/' + filename + '.txt'
    try:
        with open(filename, 'r') as f:
            content = f.read()
            user = sina_weibo('1523456657')
            user.get_basic_info(content)
    except:
        print 'Error occurs while reading file.'

    user.display_basic_info()

    user.get_weibo_content(filename)
    #user.display_weibo_content()
    user.save2markdown()

else:
    print '\n\n' + '-'*40 + '\n'
    username = raw_input('请输入用户名:\n')
    password = raw_input('请输入密码：\n')
    print '\n'
    weibo_crawler = WapWeiboCrawler(username, password)
    weibo_crawler.log_in()

    user_id = '1523456657'
    user_id = '1654301217'
    user = sina_weibo(user_id)
    home_page = weibo_crawler.get_homepage(user.user_id)
    user.get_basic_info(home_page)
    user.display_basic_info()

    page_num = raw_input('请输入需要获取的页数：')
    filename = weibo_crawler.get_content(user.user_id, user.basic_info['username'], int(page_num))

    user.get_weibo_content(filename)
    #user.display_weibo_content()
    user.save2markdown()


