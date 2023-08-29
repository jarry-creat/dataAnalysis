#!/usr/bin/env python
# encoding: utf-8
'''
@author: DeltaF
@software: pycharm
@file: 7.2Requests库入门.py
@desc:
'''

# 导入模块
import requests

# 定义url
url_douban_movie = "https://movie.douban.com/"
# headers
headers = {'user-agent': 'my-app/0.0.1'}
# 访问、并获取网页信息
# response 响应 request 请求
response_douban_movice = requests.get(
    url=url_douban_movie, headers=headers)
print(response_douban_movice.text)

# XX电影主页
url2 = "https://movie.douban.com/subject/34961898"
response2 = requests.get(url=url2, headers=headers)
print(response2.text)

# 百度百科
url3 = "https://baike.baidu.com"
response3 = requests.get(url=url3, headers=headers)
print(response3.text)