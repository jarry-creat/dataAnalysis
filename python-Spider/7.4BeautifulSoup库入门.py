#!/usr/bin/env python
# encoding: utf-8
'''
@author: DeltaF
@software: pycharm
@file: 7.4BeautifulSoup库入门.py
@desc:
'''

import requests
from bs4 import BeautifulSoup

# 获取网页全部信息
url_douban_movie = "https://movie.douban.com/subject/1292064/"
headers = {'user-agent': 'my-app/0.0.1'}
response = requests.get(url=url_douban_movie, headers=headers)
# print(response.text)

print("\n------------------------\n")

# 解析网页
soup = BeautifulSoup(response.text, 'html.parser')
print(soup.prettify())

# 提取目标消息
print(soup.title.string)  # 标题
print(soup.find_all(property="v:summary")[0].text)  # name="intro"
