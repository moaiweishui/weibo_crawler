# WeiboCrawler
通过模拟登陆的方式抓取指定微博用户的微博内容，进行分析/可视化

## Introduction
- Python 2.X

## Project framework
- **main.py**：主函数
- **wap_weibo_crawler.py**：模拟登陆[新浪微博](https://weibo.cn)（wap站），无需验证码，静态爬取
- **sina_weibo.py**：新浪微博类，其实例代表一个特定用户的新浪微博
- **content_parsing_tool.py**：内容解析/信息提取
- **seed_user_db.py**：数据库交互：种子用户（爬取目标用户）数据表

## Todo
- [ ] 优化对微博内容中存在的超链接的解析
- [x] 在获取页面时，小几率出现未能加载出微博内容的情况，导致漏掉部分微博
- [ ] 提高图片抓取的准确率
- [x] 分组可见信息的提取
- [x] 转发信息的解析
- [ ] 地理位置提取
- [x] 引入pd.DataFrame来作为保存微博条目的数据结构
- [x] matplotlib全局显示中文
<br/>

- [ ] 加入账号本身微博信息的提取
- [ ] 原图/多图
- [ ] 评论内容
- [ ] 粉丝
<br/>

- [x] 用户微博时间线的分布(还有待完善)
- [x] 24小时内，所有微博时间点分布的统计
- [ ] 以所有微博为横轴，利用柱状图/散点图展示评论/点赞数量的分布
- [ ] 饼图，展示各微博类型占比，纯文字/带图/转发
- [ ] 微博客户端来源，官方客户端/网页/第三方客户端，饼图展示占比，时间线展示变迁
<br/>

- [ ] 加入数据库/MySQL
- [ ] 建立一张数据表，存储一定数量的微博小号账号/密码信息，作为模拟登陆的入口，降低风险
- [x] 建立一张数据表，用于存储seed user，即爬取的目标用户
