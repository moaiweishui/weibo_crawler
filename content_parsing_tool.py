# coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import re


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


def get_weibo_content(filename):
    try:
        # Open local file.
        f = open(filename, 'r')
        print '-'*40 + '\n'
        print '开始解析微博内容...\n'
        content = f.read()
        # Match weibo entry. 
        pattern = re.compile('<div class="c" id=".*?">.*?<div>.*?<span class="ctt">(.*?)</span>.*?<a href="https://weibo.cn/attitude.*?">(.*?)</a>.*?<a href="https://weibo.cn/repost.*?">(.*?)</a>.*?<a class="cc" href="https://weibo.cn/comment.*?">(.*?)</a>.*?<span class="ct">(.*?)</span>.*?</div>.*?</div>', re.S)
        entrys = re.findall(pattern, content)
        cnt = 1
        result = list()
        if entrys:
            print '共获取到%d条微博。' % (len(entrys))
            for entry in entrys:
                weibo = dict()
                weibo['cnt'] = cnt
                weibo['content'] = entry[0].strip()
                # Match hyperlink.
                pattern = re.compile('<a href="(.*?)">(.*?)</a>', re.S)
                hyperlink = re.findall(pattern, weibo['content'].encode('utf-8'))
                # If this weibo entry include hyperlink.
                if hyperlink:
                    # Remove redundant spacing and line break.
                    pattern = re.compile('(.*?)<a href="(.*?)">(.*?)</a>(.*?)', re.S)
                    hyperlink_content = re.findall(pattern, weibo['content'].encode('utf-8'))
                    weibo['content'] = ''
                    for x in hyperlink_content:
                        weibo['content'] = weibo['content'] + x[0].strip() + '<a href="' + x[1].strip() + '">' + x[2].strip() + '</a>' + x[3]
                weibo['attitude'] = entry[1].strip()
                weibo['repost'] = entry[2].strip()
                weibo['comment'] = entry[3].strip()
                weibo['time'] = entry[4].strip()
                result.append(weibo)
                cnt = cnt + 1
        else:
            print '未能获取到微博内容。'
    finally:
        f.close()
    
    return result
    


