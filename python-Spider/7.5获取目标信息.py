#!/usr/bin/env python
# encoding: utf-8
'''
@author: DeltaF
@software: pycharm
@file: 7.5获取目标信息.py
@desc:
'''
import requests
from bs4 import BeautifulSoup


def get_list(soup_list):
    """
    清洗解析后的网页信息，并以列表形式返回
    :param soup_list:  bs_list
    :return:  list
    """
    list = []
    for ele in soup_list:
        list.append(ele.string)
    return list


# 访问网页、获取信息
url_douban_movie = "https://movie.douban.com/subject/1292064/"
headers = {'user-agent': 'my-app/0.0.1'}
response = requests.get(url=url_douban_movie, headers=headers)
# print(response.text)

print("\n------------------------\n")

# 获取目标信息
soup = BeautifulSoup(response.text, 'html.parser')
# print(soup.prettify())

# 存储容器，电影信息一览
movie_info = {}

# 电影名称
movie_info['title'] = soup.find(property="v:itemreviewed").string

# 简介部分
movie_info['director'] = soup.find(rel="v:directedBy").string  # 导演
movie_info['writer'] = soup.find_all(class_="attrs")[1].string  # 编剧
movie_info['actors'] = get_list(soup.find_all(rel="v:starring"))  # 演员列表
movie_info['genre'] = get_list(soup.find_all(property="v:genre"))  # 类型
movie_info['language'] = soup.find(text="语言:").next_element  # 语言
movie_info['release_date'] = soup.find(property="v:initialReleaseDate").string  # 发行日
movie_info['runtime'] = soup.find(property="v:runtime").string  # 时长

# 评分部分
movie_info['average'] = soup.find(property="v:average").string
movie_info['votes'] = soup.find(property="v:votes").string

for key in movie_info:
    print(key, ":", movie_info.get(key))
