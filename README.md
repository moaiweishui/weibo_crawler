# WeiboCrawler
通过模拟登陆的方式对指定微博用户微博进行爬取

## Introduction
- Python 2.X

## Project framework
- **main.py**：主函数
- **wap_weibo_crawler.py**：模拟登陆[新浪微博](https://weibo.cn)（wap站），无需验证码，静态爬取
- **sina_weibo.py**：新浪微博类，其实例代表一个特定用户的新浪微博
- **content_parsing_tool.py**：内容解析/信息提取

## Todo
- 优化对微博内容中存在的超链接的解析
- 在获取页面时，小几率出现未能加载出微博内容的情况，导致漏掉部分微博
- 提高图片抓取的准确率
- 分组可见信息的提取
- 转发信息的解析
- 地理位置提取
<br/>

- 原图/多图
- 评论内容
