# coding=utf-8

import sys
import time
import random

import requests
from bs4 import BeautifulSoup

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
            print "模拟登陆成功,当前登陆账号为：" + username
        else:
            print "模拟登陆失败"
    
    def get_page(self, url):
        page = self.session.get(url)
        print "Get page succeed:",
        print page.url
        return page.content

    def get_content(self):
        filename = raw_input('请输入文件名:\n')
        f = open(filename, 'w')
        user_id = raw_input('请输入需要爬取的用户ID:\n')
        baseURL = 'https://weibo.cn/u/' + user_id
        page_number = raw_input('请输入需要爬取的页数:\n')
        for i in range(int(page_number)):
            url = baseURL + '?page=' + str(i+1)
            time.sleep(2)
            page = self.get_page(url)
            soup = BeautifulSoup(page, 'lxml')
            f.write(soup.prettify())
        f.close()


if __name__ == '__main__':
    username = raw_input('请输入用户名:\n')
    password = raw_input('请输入密码：\n')
    weibo_crawler = WapWeiboCrawler(username, password)
    weibo_crawler.log_in()
    weibo_crawler.get_content()





