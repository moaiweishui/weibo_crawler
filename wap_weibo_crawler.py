# coding=utf-8

import sys
import time
import random
import re

import requests
from bs4 import BeautifulSoup

from sina_weibo import *

reload(sys)
sys.setdefaultencoding("utf-8")

class WapWeiboCrawler():
    def __init__(self, username, password):
        self.user_agents = [
                'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKi    t/601.1.46 (KHTML, like Gecko) Version/9.0 '
                'Mobile/13B143 Safari/601.1]',
                'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWeb    Kit/537.36 (KHTML, like Gecko) '
                'Chrome/48.0.2564.23 Mobile Safari/537.36',
                'Mozilla/5.0 (Linux; Android 5.1.1; Nexus 6 Build/LYZ28E) AppleWe    bKit/537.36 (KHTML, like Gecko) '
                'Chrome/48.0.2564.23 Mobile Safari/537.36']
        self.headers = {
                'User_Agent': random.choice(self.user_agents),
                'Referer': 'https://passport.weibo.cn/signin/login?entry=mwei    bo&res=wel&wm=3349&r=http%3A%2F%2Fm.weibo.cn%2F',
                'Origin': 'https://passport.weibo.cn',
                'Host': 'passport.weibo.cn'}
        self.post_data = {
                'username': '',
                'password': '',
                'savestate': '1',
                'ec': '0',
                'pagerefer': 'https://passport.weibo.cn/signin/welcome?entry=    mweibo&r=http%3A%2F%2Fm.weibo.cn%2F&wm=3349&vt=4',
                'entry': 'mweibo'}
        self.login_url = 'https://passport.weibo.cn/sso/login'
        self.username = username
        self.password = password
        self.session = requests.session()

    def log_in(self):
        self.post_data['username'] = self.username
        self.post_data['password'] = self.password
        response = self.session.post(self.login_url, data=self.post_data, headers=self.headers)
        if response.status_code == 200:
            print "模拟登陆成功,当前登陆账号为：" + self.username
        else:
            raise Exception("模拟登陆失败")
    
    def get_page(self, url):
        page = self.session.get(url)
        return page.content

    def get_homepage(self, user_id):
        baseURL = 'https://weibo.cn/u/' + user_id
        home_page = BeautifulSoup(self.get_page(baseURL), 'lxml').prettify()
        return home_page

    def get_content(self, user_id, page_num):
        print '\n----------------------------------------\n'
        print '开始获取ID为%s用户的前%d页微博内容...\n' % (user_id, page_num)
        filename = raw_input('请输入你要保存的文件名: ')
        try:
            f = open(filename, 'w')
            base_url = 'https://weibo.cn/u/' + user_id
            for i in range(int(page_num)):
                url = base_url + '?page=' + str(i+1)
                time.sleep(2)
                page = self.get_page(url)
                if page:
                    print "Get page succeed:",
                    print url
                    soup = BeautifulSoup(page, 'lxml')
                    f.write(soup.prettify())
                else:
                    print "Get page failed."
        finally:
            f.close()
        return filename


if __name__ == '__main__':
    username = raw_input('请输入用户名:\n')
    password = raw_input('请输入密码：\n')
    weibo_crawler = WapWeiboCrawler(username, password)
    weibo_crawler.log_in()
    
    user_id = '1523456657'
    user = sina_weibo(user_id)
    home_page = weibo_crawler.get_homepage(user.user_id)
    user.get_basic_info(home_page)
    user.display_basic_info()
    
    filename = weibo_crawler.get_content(user.user_id, 2)

