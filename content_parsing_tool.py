# coding=utf-8
import sys
import traceback

reload(sys)
sys.setdefaultencoding("utf-8")

import re
from datetime import datetime


def get_basic_info(homepage_content):
    basic_info = dict()
    content = homepage_content.encode('utf-8')

    # Get username/sex/region/relationship/signature.
    pattern = re.compile('<span class="ctt">(.*?)<span class="cmt">(.*?)</span>.*?<span class="ctt".*?>(.*?)</span>', re.S)
    result = re.search(pattern, content)
    if result:
        # \xc2\xa0: Non-breaking space
        basic_info['username'] = result.group(1).strip().split('\xc2\xa0')[0]
        basic_info['sex'] = result.group(1).strip().split('\xc2\xa0')[1].split('/')[0]
        basic_info['region'] = result.group(1).strip().split('\xc2\xa0')[1].split('/')[1]
        basic_info['relationship'] = result.group(2).strip()
        basic_info['signature'] = result.group(3).strip()
    else:
        None
    
    # Get weibo number/follow/fans.
    pattern = re.compile('<span class="tc">(.*?)</span>.*?<a href="/.*?/follow">(.*?)</a>.*?<a href="/.*?/fans">(.*?)</a>', re.S)
    result = re.search(pattern, content)
    if result:
        basic_info['weibo_num'] = result.group(1).strip()
        basic_info['follow'] = result.group(2).strip()
        basic_info['fans'] = result.group(3).strip()
    else:
        None

    # Get page number.
    pattern = re.compile('<input type="submit" value="跳页"/>(.*?)</div>', re.S)
    result = re.search(pattern, content)
    if result:
        basic_info['page_num'] = re.match(r'.*?/(\d+).*?', result.group(1).strip()).group(1)
    else:
        None

    return basic_info


def get_weibo_content(filename, current_time):
    try:
        # Open local file.
        with open(filename, 'r') as f:
            print '-'*40 + '\n'
            print '开始解析微博内容...\n'
            content = f.read()
            
            # Match weibo entry. 
            pattern = re.compile('<div class="c" id=".*?">.*?<div>(.*?)<span class="ctt">(.*?)</span>(.*?)<a href="https://weibo.cn/attitude.*?">(.*?)</a>(.*?[<a href="https://weibo.cn/repost.*?">.*?</a>|<span class="cmt">.*?</span>].*?)<a class="cc" href="https://weibo.cn/comment(.*?)">(.*?)</a>.*?<span class="ct">(.*?)</span>.*?</div>.*?</div>.*?<div class="s">.*?</div>', re.S)
            entrys = re.findall(pattern, content)
            cnt = 1
            result = list()
            if entrys:
                print '共获取到%d条微博。' % (len(entrys))
                for entry in entrys:
                    weibo = dict()
                    weibo['cnt'] = cnt
                    weibo['repost_info'] = entry[0].strip()
                    weibo['repost_info'] =  weibo_parsing_repost_info(weibo['repost_info'].encode('utf-8'))

                    weibo['content'] = entry[1].strip()
                    
                    # Parsing hyperlink.
                    weibo['content'] = weibo_parsing_hyperlink(weibo['content'].encode('utf-8'))

                    # If this weibo entry include picture.
                    weibo['pic'] = entry[2].strip()
                    if weibo['pic']:
                        pattern = re.compile('.*?<a href="https://weibo.cn/mblog/pic(.*?)">.*?<img.*?src="(.*?)"/>.*?</a>.*?', re.S)
                        pic_content = re.findall(pattern, weibo['pic'].encode('utf-8'))
                        for x in pic_content:
                            weibo['origin_pic_url'] = 'https://weibo.cn/mblog/pic' + x[0]
                            weibo['pic'] = x[1]
                    else:
                        del weibo['pic']
                        
                    weibo['attitude'] = entry[3].strip()
                    
                    # Parsing repost.
                    weibo['repost'] = entry[4].strip()
                    weibo['repost'] = weibo_parsing_repost(weibo['repost'].encode('utf-8'))
                        
                    # Url where include origin comment information.
                    weibo['comment_url'] = 'https://weibo.cn/comment' + entry[5].strip()
                    weibo['comment'] = entry[6].strip()
                    weibo['time'] = entry[7].strip()
                    weibo['time'], weibo['from'] = weibo_parsing_time_from(weibo['time'], current_time)
                    result.append(weibo)
                    cnt = cnt + 1
            else:
                print '未能获取到微博内容。'
    except Exception, e:
        print 'Error occurs while reading file.'
        traceback.print_exc()
        print traceback.format_exc()
    
    return result



# Parsing repost information    
def weibo_parsing_repost_info(repost_info):
    res = ''
    if repost_info:
        # Match repost information
        pattern = re.compile('<span class="cmt">.*?<a href="(.*?)">(.*?)</a>.*?</span>', re.S)
        find_res = re.findall(pattern, repost_info)
        # If this weibo is repost from another one.
        for x in find_res:
            # repost source url
            res += x[0].strip()
            res += '|'
            # repost source name
            res += x[1].strip()
    else:
        res = 'None repost'
    return res


# Parsing hyperlink in weibo entry.
def weibo_parsing_hyperlink(weibo_content):
    # Match hyperlink
    pattern = re.compile('<a href="(.*?)">(.*?)</a>', re.S)
    hyperlink = re.findall(pattern, weibo_content)
    # If this weibo entry include hyperlink.
    if hyperlink:
        # Remove redundant spacing and line break.
        pattern = re.compile('(.*?)<a href="(.*?)">(.*?)</a>(.*?)', re.S)
        hyperlink_content = re.findall(pattern, weibo_content)
        result= ''
        for x in hyperlink_content:
            result = result + x[0].strip() + '<a href="' + x[1].strip() + '">' + x[2].strip() + '</a>' + x[3]
    else:
        result = weibo_content

    return result
    

# Parsing repost information in weibo entry.
def weibo_parsing_repost(weibo_repost):
    # Match repost forbidden.
    pattern = re.compile('<span class="cmt">(.*?)</span>', re.S)
    forbid_repost = re.findall(pattern, weibo_repost)
    # If this weibo forbid repost.
    if forbid_repost:
        result = forbid_repost[0].strip()
    else:
        pattern = re.compile('<a href="https://weibo.cn/repost.*?">(.*?)</a>', re.S)
        result = re.findall(pattern, weibo_repost)[0].strip()

    return result


# Parsing time and from
def weibo_parsing_time_from(weibo_time, current_time):
    _list = []
    # Date
    _list.append(weibo_time.split(' ', 1)[0])
    # Time
    _list.append(weibo_time.split(' ', 1)[1].split('\xc2\xa0', 1)[0])
    # From
    _list.append(weibo_time.split(' ', 1)[1].split('\xc2\xa0', 1)[1])

    if _list[0] == '今天':
        month = str(current_time.month)
        day = str(current_time.day)
        if len(month) == 1:
            month = '0' + month
        if len(day) == 1:
            day = '0' + day
        _date_time = str(current_time.year) + '-'\
                + month + '-'\
                + day
        _date_time = _date_time + ' ' + _list[1]
        _date_time = datetime.strptime(_date_time, '%Y-%m-%d %H:%M')
    elif len(_list[0].split('-')) == 1:
        pattern = re.compile('(.*?)月(.*?)日', re.S)
        result = re.search(pattern, _list[0])
        month = result.group(1)
        day = result.group(2)
        _date_time = str(current_time.year) + '-'\
                + month + '-'\
                + day
        _date_time = _date_time + ' ' + _list[1]
        _date_time = datetime.strptime(_date_time, '%Y-%m-%d %H:%M')
    else:
        _date_time = _list[0] + ' ' + _list[1]
        _date_time = datetime.strptime(_date_time, '%Y-%m-%d %H:%M:%S')
    #datetime.strptime(_date_time, '%Y-%m-%d %H:%M')
    pattern = re.compile('.*?<a href.*?>(.*?)</a>.*?', re.S)
    result = re.search(pattern, _list[2])
    if result:
        _from = result.group(1).strip()
    else:
        _from = _list[2]
    # Must use greedy mode
    pattern = re.compile('来自(.*)', re.S)
    result = re.search(pattern, _from)
    if result:
        _from = result.group(1).strip()
        None

    return _date_time, _from
    

# Extract numeric value from input text.
def numeric_value_extration(input_text):
    pattern = re.compile('(.*?)\[(.*?)\]', re.S)
    result = re.search(pattern, input_text)
    if result.group(1) in ['赞', '转发', '评论']:
        return int(result.group(2).strip())
    else:
        return 'Input text do not have numeric value.'
