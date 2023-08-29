#!/usr/bin/env python
# encoding: utf-8
'''
@author: DeltaF
@software: pycharm
@file: 7.9练习：按标签获取电影数据.py
@desc:
'''

import requests
from bs4 import BeautifulSoup
import pandas as pd

headers = {'user-agent': 'my-app/0.0.1'}
movie_links = []
movie_names = []
all_infos = []
movie_lists = []


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
def get_page(page_link, tag, genre):
    page = 0
    max_page = 100  # start参数对应的值，也就是说第10页对应的start值
    while page <= max_page:
        # 访问页面
        url = page_link + "tags=" + tag + "&start=" + page.__str__() + "&genres=" + genre
        response = requests.get(url=url, headers=headers)
        print(response.text)
        movie_info = response.text
        # 将获取到的string转为字典
        movie_info = eval(movie_info)  # eval() = dict()
        # 转出到列表中
        for m in movie_info['data']:
            movie_lists.append(m)  # m是字典类型的数据
            url_str = m.get('url')  # 处理url，将\/替换为/
            movie_links.append(url_str.replace('\/', '/'))
        # 修改start参数
        page += 20
        # 验证数据正确性
        print(url)


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
        movie_info['writer'] = get_list(soup.find_all(class_="attrs")[1].find_all('a')) if len(writer) > 1 else ""  # 编剧
        movie_info['actors'] = get_list(soup.find_all(rel="v:starring"))  # 演员列表
        movie_info['genre'] = get_list(soup.find_all(property="v:genre"))  # 类型
        movie_info['language'] = soup.find(text="语言:").next_element  # 语言
        movie_info['release_date'] = soup.find(property="v:initialReleaseDate").string  # 发行日
        movie_info['runtime'] = soup.find(property="v:runtime").string  # 时长
        # 评分部分
        movie_info['average'] = soup.find(property="v:average").string
        movie_info['votes'] = soup.find(property="v:votes").string
        # 链接
        movie_info['link'] = url
        # 打印信息
        for key in movie_info:
            print(key, ":", movie_info.get(key))
    except AttributeError:
        print("电影已下架")

    # 电影信息存到列表中
    all_infos.append(movie_info)


# start=0&genres=%E6%82%AC%E7%96%91
if __name__ == '__main__':
    get_page("https://movie.douban.com/j/new_search_subjects?"
             "sort=U&range=0,10&", tag="电影", genre="爱情")
    # 调用获取详细信息的方法
    for l in movie_links:
        print("正在抓取电影：", l)
        get_infos(url=l)
    # 拿到{}电影信息，list.append存储容器中，list>dataframe > to_excel
    data = pd.DataFrame(all_infos)
    data.to_excel("API标签参数获取电影数据.xlsx")
