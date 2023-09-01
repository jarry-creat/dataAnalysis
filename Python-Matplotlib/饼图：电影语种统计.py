import C8处理与分析.pandas_def as pdef
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
# 获取统计数据
data = pdef.language_tj()
# print(data)

# 对数据进行排序
data = data.sort_values('tj', ascending=False)
print(data)

# 绘制饼图
data = data.iloc[0:20]
labels = data.index
sizes = data['tj'].tolist()

plt.pie(x=sizes, labels=labels, autopct='%1.1f%%', startangle=90)
plt.title(u'电影语种统计')
plt.legend(title="Ingredients",
           loc="center left",
           bbox_to_anchor=(1, 0, 0.5, 1))
plt.show()
