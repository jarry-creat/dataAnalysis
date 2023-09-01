import pandas_def as pdef
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
# 获取数据
'''
x轴：年份 -> 找到近5年的数据，2015年~2020年
y轴：评分数据
'''
year_list = ['2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020']
data = pdef.rate_tj_by_year(year_list)

# 绘制箱线图
plt.boxplot(data, labels=year_list)
plt.title('每年电影评分变化')
plt.xlabel('年份2015~2020')
plt.ylabel('评分数据')
plt.show()
