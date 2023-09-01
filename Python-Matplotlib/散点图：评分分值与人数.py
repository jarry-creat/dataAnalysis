import C8处理与分析.pandas_def as pdef
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
# 获取数据：average，votes
data = pdef.averge_votes()
# print(data)

# 绘制图表
plt.scatter(x=data['average'], y=data['votes'])
title = len(data).__str__() + " 部电影评分分值与人数"
plt.title(title)
plt.xlabel('评分分值')
plt.ylabel('评价人数')
plt.grid()
plt.show()

# 筛选、排序 -> 结合图表，观察数据
print("====================高分热门电影====================")
print(data.sort_values(['votes', 'average'], ascending=False).head(20))
