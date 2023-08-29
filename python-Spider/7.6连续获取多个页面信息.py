#!/usr/bin/env python
# encoding: utf-8
'''
@author: DeltaF
@software: pycharm
@file: 7.6连续获取多个页面信息.py
@desc:
'''
import requests
from bs4 import BeautifulSoup

# 访问top250主页
# 访问网页、获取信息
headers = {'user-agent': 'my-app/0.0.1'}

# 跳转页面 ?start=225&filter=
# 我先访问url链接，加上参数0，25，50，75~~225
page = 0
max_page = 225  # start参数对应的值，也就是说第10页对应的start值
movie_links = []
movie_names = []
while page <= max_page:
    # 访问页面
    url = "https://movie.douban.com/top250?start=" + page.__str__() + "&filter="
    response = requests.get(url=url, headers=headers)
    # print(response.text)
    # 实现每个页面信息的抓取：电影单链
    soup = BeautifulSoup(response.text, 'html.parser')
    # print(soup.find_all(class_="hd"))
    for ele in soup.find_all(class_="hd"):
        movie_names.append(ele.find(class_="title").string)
        movie_links.append(ele.find('a', href=True).attrs['href'])
    # 修改start参数
    page += 25
    # 验证数据正确性
    print(url)
    # 退出
    # exit()

# 浏览所有抓取到的信息
for name, link in zip(movie_names, movie_links):
    print(name, ":", link)
