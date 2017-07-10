# -*- coding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from content_parsing_tool import *
from sina_weibo import *

filename = raw_input('请输入文件名:\n')
try:
    f = open(filename, 'r')
    content = f.read()
    user_weibo = sina_weibo('1523456657', 'weibo.cn', content)
finally:
    f.close()

user_weibo.get_basic_info()
user_weibo.display_basic_info()
