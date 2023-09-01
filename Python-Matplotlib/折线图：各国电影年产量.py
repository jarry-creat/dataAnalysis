import pandas_def as pdef
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']

# 获取统计数据：模块化 -> def
data = pdef.country_year_tj()
print(data)

# 绘制折线图
data.plot()
plt.legend(ncol=4)
plt.title('各国电影年产量')
plt.xlabel('年份')
plt.ylabel('数量')
plt.show()

# 创建直方图
# plt.bar(data.columns, "各国总电影量", 0.5)  # DF[LABEL].SUM()
# plt.show()
