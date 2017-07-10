# WeiboCrawler
通过模拟登陆的方式对指定微博用户微博进行爬取

## Introduction
- Python 2.X

## Project framework
- **main.py**：主函数
- **wap_weibo_crawler.py**：模拟登陆[新浪微博](https://weibo.cn)（wap站），无需验证码，静态爬取
- **sina_weibo.py**：新浪微博类，其实例代表一个特定用户的新浪微博
- **content_parsing_tool.py**：内容解析/信息提取
