# coding=utf-8

import sys
import os

from content_parsing_tool import *

reload(sys)
sys.setdefaultencoding("utf-8")

class sina_weibo():
    def __init__(self, user_id):
        self.user_id = user_id
        self.basic_info = dict()
        self.weibo_content = list()

    def get_basic_info(self, home_page):
        self.basic_info = get_basic_info(home_page)

    def display_basic_info(self):
        print '\n' + '-'*40 + '\n'
        print '昵称：' + self.basic_info['username'] + '    ',
        print self.basic_info['sex'] + '/' + self.basic_info['region'] + '\n'
        print self.basic_info['weibo_num'] + '  |  ',
        print self.basic_info['follow'] + '  |  ',
        print self.basic_info['fans'] + '\n'
        print '简介：' + self.basic_info['signature']
        print '\n共有微博内容%d页' % (int(self.basic_info['page_num']))
        print '\n' + '-'*40 + '\n'

    def get_weibo_content(self, filename):
        self.weibo_content = get_weibo_content(filename)

    def display_weibo_content(self):
        for weibo in self.weibo_content:
            print '\n' + '-'*40
            print weibo['cnt'], weibo['time']
            print weibo['content']
            print weibo['pic']
            print weibo['attitude'] + '  ',
            print weibo['repost'] + '  ',
            print weibo['comment'] + '  '
            print '\n\n'

    def save2markdown(self):
        filename = self.basic_info['username'] + '.md'
        dir_path = 'output file/' + self.basic_info['username'] + '/'
        # If folder does not exist.
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
            print 'Create fold: "' + dir_path + '" succeed.'
        filename = dir_path + filename
        bp = '&nbsp;&nbsp;'
        try:
            with open(filename, 'w') as f:
                print '\n' + '-'*40 + '\n'
                print '开始写入Markdown文件...\n'
                line_list = list()
                #line_list.append('### Basic information:\n')
                line_list.append('- 昵称：' + self.basic_info['username'] + bp*6)
                line_list.append(self.basic_info['sex'] + '/' + self.basic_info['region'] + '\n\n')
                line_list.append('- ' + self.basic_info['weibo_num'] + bp*4 + '|' + bp*4)
                line_list.append(self.basic_info['follow'] +  bp*4 + '|' + bp*4)
                line_list.append(self.basic_info['fans'] + '\n')
                f.writelines(line_list)

                line_list = []
                #line_list.append('\n\n### Weibo content:\n')
                cnt = 0
                for weibo in self.weibo_content:
                    cnt = cnt + 1
                    line_list.append('***\n')
                    line_list.append('> ' + str(weibo['cnt']) + bp*3)
                    line_list.append(weibo['time'] + '\n\n')
                    line_list.append('> ' + weibo['content'] + '\n\n')
                    # If include pic
                    if weibo['pic']:
                        line_list.append('> [![' + weibo['pic'] + '](' + weibo['pic'] + ')](' +weibo['origin_pic_url'] + ')\n\n')
                    line_list.append('> ' + weibo['attitude'] + '  ')
                    line_list.append(weibo['repost'] + '  ')
                    line_list.append(weibo['comment'] + '  ')
                    line_list.append('\n\n')

                f.writelines(line_list)
        except:
            print 'Error occurs while writing file.'

        print '成功生成Markdown文件，保存于： ' + filename
        print '\n' + '-'*40 + '\n\n'
