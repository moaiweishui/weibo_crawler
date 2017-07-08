# coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import re


def get_basic_info(content):
    basic_info = dict()

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

