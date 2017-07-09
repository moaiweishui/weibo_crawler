# -*- coding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from content_parsing_tool import *

filename = raw_input('请输入文件名:\n')
try:
    f = open(filename, 'r')
    content = f.read()
    basic_info = get_basic_info(content)
    for key, values in basic_info.items():
        print key + ':' + values
    print type(basic_info['page_num']), int(basic_info['page_num'])
finally:
    f.close()
