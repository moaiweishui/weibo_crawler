# coding=utf-8

import sys
import os
from datetime import datetime

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as dates
import matplotlib
import numpy as np

from content_parsing_tool import *

reload(sys)
sys.setdefaultencoding("utf-8")

zhfont = matplotlib.font_manager.FontProperties(fname='/home/liuyx/anaconda2/lib/python2.7/site-packages/matplotlib/mpl-data/fonts/ttf/msyh.ttf')
plt.rcParams['font.sans-serif'] = ['msyh']
plt.rcParams['axes.unicode_minus'] = False

class sina_weibo():
    def __init__(self, user_id):
        self.current_time = datetime.now()
        self.user_id = user_id
        self.basic_info = dict()
        self.weibo_content = list()
        self.weibo_df = pd.DataFrame(columns=['cnt',\
                'time',\
                'from',\
                'content',\
                'attitude',\
                'repost',\
                'comment'])

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
    
    # Fill weibo_content(type:list) and weibo_df(type:pd.dataframe).
    def get_weibo_content(self, filename):
        self.weibo_content = get_weibo_content(filename, self.current_time)
        for weibo in self.weibo_content:
            _list = list()
            _list.append(weibo['cnt'])
            _list.append(weibo['time'])
            _list.append(weibo['from'])
            _list.append(weibo['content'])
            # Extract numeric value from attitude/repost/comment text.
            _list.append(numeric_value_extration(weibo['attitude']))
            _list.append(numeric_value_extration(weibo['repost']))
            _list.append(numeric_value_extration(weibo['comment']))
            self.weibo_df.loc[int(weibo['cnt'])] = _list
        # Convert float64 to int64
        self.weibo_df['attitude'] = self.weibo_df['attitude'].astype(int)
        self.weibo_df['repost'] = self.weibo_df['repost'].astype(int)
        self.weibo_df['comment'] = self.weibo_df['comment'].astype(int)

        
    def display_weibo_content(self):
        for weibo in self.weibo_content:
            print '\n' + '-'*40
            print weibo['cnt'], weibo['time']
            print weibo['content']
            # If include pic 
            if 'pic' in weibo.keys() and 'origin_pic_url' in weibo.keys():
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
                print 'Write basic information to markdown file succeed.\n'
                cnt = 0
                for weibo in self.weibo_content:
                    cnt = cnt + 1
                    line_list2 = list()
                    line_list2.append('***\n')
                    line_list2.append('> ' + str(weibo['cnt']) + bp*3)
                    line_list2.append(str(weibo['time']) +' ' + weibo['from'] + '\n\n')
                    line_list2.append('> ' + weibo['content'] + '\n\n')
                    # If include pic
                    if 'pic' in weibo.keys() and 'origin_pic_url' in weibo.keys():
                        line_list2.append('> [![' + weibo['pic'] + '](' + weibo['pic'] + ')](' +weibo['origin_pic_url'] + ')\n\n')
                    line_list2.append('> ' + weibo['attitude'] + '  ')
                    line_list2.append(weibo['repost'] + '  ')
                    line_list2.append(weibo['comment'] + '  ')
                    line_list2.append('\n\n')
                    f.writelines(line_list2)

                print 'Write weibo content to markdown file succeed.\n'
                print '成功生成Markdown文件，保存于： ' + filename
                print '\n' + '-'*40 + '\n\n'
        except:
            print 'Error occurs while writing file.'

    def save2csv(self):
        #print self.weibo_df.loc[:, ['time', 'from', 'attitude', 'repost', 'comment']].head(10)
        #print self.weibo_df.loc[:, ['time', 'from', 'attitude', 'repost', 'comment']].tail(10)
        filename = self.basic_info['username'] + '.csv'
        dir_path = 'output file/' + self.basic_info['username'] + '/'
        # If folder does not exist.
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
            print 'Create fold: "' + dir_path + '" succeed.'
        filename = dir_path + filename
        print '\n' + '-'*40 + '\n'
        print '开始写入csv文件...\n'
        self.weibo_df.to_csv(filename, index=False)
        print '成功生成csv文件，保存于： ' + filename
        print '\n' + '-'*40 + '\n\n'

    # Display the weibo cnt-time chart
    def display_time_distribution(self):
        _time_series = self.weibo_df['time'].astype(str)
        date_range = pd.date_range(_time_series[len(_time_series)], _time_series[1], freq='M').values
        date_delta = int(len(date_range)/15)
        date_list = []
        date_label_list = []
        cnt = 0
        for date in date_range:
            if cnt % date_delta == 0:
                date_list.append(date)
                date_label_list.append('-'.join(str(date).split('T')[0].split('-')[0:2]))
            cnt += 1
        distribution_in_day = _time_series.apply(lambda x: int(x.split()[1].split(':')[0])).value_counts()

        fig, ax = plt.subplots(2, 1, figsize=(6, 6))

        # Display weibo quantity growth curve(All time)
        ax[0].set_title('Weibo quantity growth curve(All time)')
        ax[0].plot_date(self.weibo_df['time'], \
                (len(self.weibo_df) - self.weibo_df['cnt']),\
                color='lawngreen',\
                markersize=1)
        ax[0].set_xticks(date_list)
        ax[0].set_xticklabels(date_label_list, rotation=300, fontsize='small')
        ax[0].set_xlabel('Date(Year-Month)')
        ax[0].set_ylabel('Weibo Number')
        
        # Display weibo send time distribution(24 Hour)
        ax[1].set_title('Weibo send time distribution(24 Hour)')
        ax[1].bar(distribution_in_day.index, distribution_in_day.values,\
                color='lawngreen')
        ax[1].set_xticks(np.linspace(0, 23, 24))
        ax[1].set_xticklabels(pd.Series(np.linspace(0, 23, 24)).astype(int).apply(lambda x: str(x)).values)
        ax[1].set_xlabel('Time(Hour)')
        ax[1].set_ylabel('Weibo Number')

        fig.subplots_adjust(hspace=0.8)

        # Save picture to local
        picname = self.basic_info['username'] + '_time_distribution.png'
        dir_path = 'output file/' + self.basic_info['username'] + '/'
        # If folder does not exist.
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
            print 'Create fold: "' + dir_path + '" succeed.'
        picname = dir_path + picname
        print '图片已保存至：' + picname
        fig.savefig(picname, dpi=200)

        plt.show()

        return

    # Display the weibo source
    def display_source_distribution(self):
        _source_series = self.weibo_df['from'].astype(str)
        _source_list =_source_series.value_counts()
        total_num = _source_list.sum()
        labels = []
        fracs = []
        cnt = 0;
        for x in _source_list.index:
            # Less than 2.5%
            if(total_num/_source_list[x] < 40):
                labels.append(x)
                fracs.append(_source_list[x])
                cnt += _source_list[x]
        labels.append('Others')
        fracs.append(total_num - cnt)

        fig, ax = plt.subplots(1, 1, figsize=(4, 4))
        ax.set_title(u'微博来源分布', fontproperties=zhfont)
        ax.pie(fracs, labels = labels)

        plt.show()

        return

