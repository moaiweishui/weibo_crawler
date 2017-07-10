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
        f = open(filename, 'r')
        content = f.read()
        pattern = re.compile('<div class="c" id=".*?">.*?<div>.*?<span class="ctt">(.*?)</span>.*?<a href="https://weibo.cn/attitude.*?">(.*?)</a>.*?<a href="https://weibo.cn/repost.*?">(.*?)</a>.*?<a class="cc" href="https://weibo.cn/comment.*?">(.*?)</a>.*?<span class="ct">(.*?)</span>.*?</div>.*?</div>', re.S)
        items = re.findall(pattern, content)
        cnt = 1
        result = list()
        if items:
            print '获取到共%d条内容。' % (len(items))
            
            for item in items:
                weibo = dict()
                weibo['cnt'] = cnt
                weibo['content'] = item[0].strip()
                pattern = re.compile('<a href="(.*?)">(.*?)</a>', re.S)
                topic = re.findall(pattern, weibo['content'].encode('utf-8'))
                if topic:
                    pattern = re.compile('(.*?)<a href="(.*?)">(.*?)</a>(.*?)', re.S)
                    processed_content = re.findall(pattern, weibo['content'].encode('utf-8'))
                    weibo['content'] = ''
                    for x in processed_content:
                        weibo['content'] = weibo['content'] + x[0].strip() + '<a href="' + x[1].strip() + '">' + x[2].strip() + '</a>' + x[3]

                weibo['attitude'] = item[1].strip()
                weibo['repost'] = item[2].strip()
                weibo['comment'] = item[3].strip()
                weibo['time'] = item[4].strip()
                result.append(weibo)
                cnt = cnt + 1
        else:
            print '未能获取到微博内容。'
    finally:
        f.close()
    
    return result
    


