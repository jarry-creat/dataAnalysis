#!/usr/bin/env python
# encoding: utf-8
'''
@author: DeltaF
@software: pycharm
@file: 7.7整合爬虫功能函数.py
@desc:
'''
import requests
from bs4 import BeautifulSoup
import pandas as pd

headers = {'user-agent': 'my-app/0.0.1'}
movie_links = []
movie_names = []


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


# 1. 访问主页面，并且完成页面跳转
def get_page(page_link):
    page = 0
    max_page = 225  # start参数对应的值，也就是说第10页对应的start值
    while page <= max_page:
        # 访问页面
        url = page_link + "?start=" + page.__str__() + "&filter="
        response = requests.get(url=url, headers=headers)
        # 获取电影链接
        get_links(response)
        # 修改start参数
        page += 25
        # 验证数据正确性
        print(url)


# 2. 抓取每个页面所有的电影链接
def get_links(response):
    soup = BeautifulSoup(response.text, 'html.parser')
    # print(soup.find_all(class_="hd"))
    for ele in soup.find_all(class_="hd"):
        movie_names.append(ele.find(class_="title").string)
        movie_links.append(ele.find('a', href=True).attrs['href'])


# 3. 根据电影链接，获取基本信息、评分信息
def get_infos(url):
    response = requests.get(url=url, headers=headers)
    # print(response.text)
    soup = BeautifulSoup(response.text, 'html.parser')
    # 存储容器，电影信息一览
    movie_info = {}
    # 容错处理
    try:
        # 电影名称
        movie_info['title'] = soup.find(property="v:itemreviewed").string
        # 简介部分
        movie_info['director'] = soup.find(rel="v:directedBy").string  # 导演
        writer = soup.find_all(class_="attrs")
        movie_info['writer'] = soup.find_all(class_="attrs")[1].string if len(writer) > 1 else ""  # 编剧
        movie_info['actors'] = get_list(soup.find_all(rel="v:starring"))  # 演员列表
        movie_info['genre'] = get_list(soup.find_all(property="v:genre"))  # 类型
        movie_info['language'] = soup.find(text="语言:").next_element  # 语言
        movie_info['release_date'] = soup.find(property="v:initialReleaseDate").string  # 发行日
        movie_info['runtime'] = soup.find(property="v:runtime").string  # 时长
        # 评分部分
        movie_info['average'] = soup.find(property="v:average").string
        movie_info['votes'] = soup.find(property="v:votes").string
        # 打印信息
        for key in movie_info:
            print(key, ":", movie_info.get(key))
    except AttributeError:
        print("电影已下架")


if __name__ == '__main__':
    # 调用功能1，实现页面的访问
    get_page(page_link="https://movie.douban.com/top250")
    # get_infos("https://movie.douban.com/subject/26430107/")
    # exit()
    # 获取所有链接
    for name, link in zip(movie_names, movie_links):
        print(name, ":", link)
        get_infos(link)  # 调用功能3，根据url爬取电影信息
