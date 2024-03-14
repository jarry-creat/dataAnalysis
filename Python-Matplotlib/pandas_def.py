import pandas as pd
import numpy as np
# 显示所有列
pd.set_option('display.max_columns', None)
# 显示所有行
pd.set_option('display.max_rows', None)
def movie_year_amount_tj():
    data = pd.read_csv("movie_data_cleaned.csv")
    # 转换为 Pandas 的 datetime64 数据类型
    data['release_date'] = pd.to_datetime(data['release_date'])
    # 这将使 release_date 列成为索引
    data = data.set_index(data['release_date'])
    # 对每个年份内的元素进行计数
    data_year_tj = data['release_date'].resample('Y').count()
    return pd.DataFrame(data_year_tj)

def country_year_tj():
    data = pd.read_csv('movie_data_cleaned.csv',
                       usecols=['title', 'country', 'language', 'release_date', 'average'])
    data = data[['title', 'country', 'language', 'release_date', 'average']]
    # 各国每年的电影产量
    data['country'] = data['country'].str.strip(' ')
    data['country'] = data['country'].fillna(value='')
    country_list = []
    for c in data['country']:
        c_list = c.split(' / ')
        for label in c_list:  # 123,2,3 -> 1,2,3
            country_list.append(label)
    country_list = list(set(country_list))
    country_list.remove('')
    country_list.remove('美国/澳大利亚')
    country_list.remove('捷克斯洛伐克/捷克')
    country_list.remove('中国大陆')  # 只统计中国
    country_list.remove('中国香港')
    country_list.remove('中国台湾')
    data['release_date'] = pd.to_datetime(data['release_date'])
    data = data.set_index(data['release_date'])
    count = 0
    tj = pd.DataFrame(data['release_date'].resample('Y').count())
    tj = tj.drop(columns='release_date')
    for label in country_list:
        temp = data[data['country'].str.contains(label)]
        print("=====================================")
        print("标签=", label)
        print("总频数=", len(temp))
        count += len(temp)
        tj[label] = temp['release_date'].resample('Y').count()
    tj = tj.fillna(value=0)
    return tj


def language_tj():
    data = pd.read_csv('movie_data_cleaned.csv',
                       usecols=['title', 'country', 'language', 'release_date', 'average'])
    data = data[['title', 'country', 'language', 'release_date', 'average']]
    # label统计 -> list
    data['language'] = data['language'].str.strip(' ')
    data['language'] = data['language'].fillna(value='')
    lang_list = []
    for l in data['language']:
        l_list = l.split(' / ')
        for label in l_list:  # 123,2,3 -> 1,2,3
            lang_list.append(label)
    lang_list = list(set(lang_list))
    lang_list.remove('')
    lang_list.remove('汉语普通话')
    # 统计每个类型标签对应的电影量/条数/频数
    data_lang_tj = pd.DataFrame(np.zeros([len(lang_list), 1]),
                                index=lang_list, columns=['tj'])  # 2列：标签，统计值tj
    for i in data['language']:
        for label in lang_list:
            if str(i).__contains__(label):
                data_lang_tj.loc[label, 'tj'] += 1
    # 将小类汇总为大类，并添加至统计df
    chinese_fy = data_lang_tj.loc['湖南话', 'tj'] + data_lang_tj.loc['北京话', 'tj']
    # print(chinese_fy)
    data_lang_tj.loc['中国方言', 'tj'] = chinese_fy
    return data_lang_tj


def averge_votes():
    return pd.read_csv('movie_data_cleaned.csv', usecols=['average', 'votes', 'title'])


def genre_tj():
    # 读取数据
    data = pd.read_csv('movie_data_cleaned.csv')
    # 获取所有类型：提取每一行的genre元素 -> 新的列表 genre_list -> 去重
    data['genre'] = data['genre'].str.strip('[')
    data['genre'] = data['genre'].str.strip(']')
    data['genre'] = data['genre'].fillna(value='')
    genre_list = []
    for g in data['genre']:
        g_list = g.split(', ')
        for label in g_list:  # 123,2,3 -> 1,2,3
            genre_list.append(label)
    g_list = list(set(genre_list))
    g_list.remove('')
    # 统计每个类型标签对应的电影量/条数/频数
    data_genre_tj = pd.DataFrame(np.zeros([len(g_list), 1]),
                                 index=g_list, columns=['tj'])  # 2列：标签，统计值tj
    for i in data['genre']:
        for label in g_list:
            if str(i).__contains__(label):
                data_genre_tj.loc[label, 'tj'] += 1
    return data_genre_tj


def genre_rates_tj(x):
    '''
    :param x: 前X为
    :return: 排名前X位的电影类型标签，对应的评分均值数据
    '''
    # 电影类型(x)：6个标签，电影数量最多的
    # 评分数据(y)：2，3，4，5，6，7，8，9，10
    # 电影数量(值）
    genre_list = genre_tj().sort_values('tj', ascending=False) \
        .head(x).index.tolist()
    rate_list = [2, 3, 4, 5, 6, 7, 8, 9, 10]
    data = pd.read_csv(file, usecols=['genre', 'average'])
    # 统计满足类型与评分区间的数据
    data_genre_tj = pd.DataFrame(np.zeros([len(rate_list), len(genre_list)]),
                                 index=rate_list, columns=genre_list)
    for g in genre_list:  # 循环遍历6个变迁元素
        for rate in rate_list:  # 循环遍历2-10评分数值
            for i, r in zip(data['genre'], data['average']):
                if str(i).__contains__(g) and rate <= r < rate + 1:
                    data_genre_tj.loc[rate, g] += 1
    return data_genre_tj


def rate_tj_by_year(year_list):
    data = pd.read_csv('movie_data_cleaned.csv',
                       usecols=['title', 'average', 'release_date'])
    data = data.set_index(pd.to_datetime(data['release_date']))
    tj = []
    for year in year_list:
        tj.append(data[year]['average'].tolist())
    return tj


if __name__ == '__main__':
    # print(movie_year_amount_tj())
    # print(genre_rates_tj(6))
    print(rate_tj_by_year(['2015', '2016']))
