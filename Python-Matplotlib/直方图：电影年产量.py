import pandas_def as pdef
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']

# 获取统计数据
tj = pdef.movie_year_amount_tj()
# print(type(tj))

# 数据的转换 dataframe -> series -> list，年份、电影产量
tj['year'] = tj.index
years = tj['year'].dt.year
amounts = tj['release_date'].tolist()
print(years)
print(amounts)
# exit()
# 绘制直方图
width = 0.35  # the width of the bars: can also be len(x) sequence
fig, ax = plt.subplots()

ax.bar(years, amounts, width)

ax.set_ylabel('电影数量')
ax.set_ylabel('年份')
ax.set_title('电影年产量')
ax.legend()

plt.show()
