
import pandas as pd
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder  # 预处理
from sklearn.cluster import KMeans  # 聚类算法
from sklearn.metrics import silhouette_score  # 用于评估度量的模块
import numpy as np
import matplotlib.pyplot as plt

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('max_colwidth', 30)
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']

# 获取到数据
data = pd.read_csv("ad_performance.csv", index_col=0)
print(data.head(2))

# 对数据进行审查：是否有缺失值
print('{:*^60}'.format('数据样本：统计描述'))
print(data.describe().round(4).T)

# 对缺失值的填充（均值）
print('{:*^60}'.format('缺失值：填充填充法'))
# print(data[data.isna().values == True])
# print(data.isna().values)
# print(data['平均停留时间'].mean)
data = data.fillna(419.77)

# 计算、合并：相关性
print('{:*^60}'.format('计算相关性：合并'))
print(data.corr().round(4).T)
# 生成相关性统计表格
# pd.DataFrame(data.corr().round(4).T).to_excel('corr.xlsx')
data = data.drop(['平均停留时间'], axis=1)
# print(data.columns)

# 数据标准化：归一化Min-Max，0-1区间
# SKLEAN-preprocessing-minmax
matrix = data.iloc[:, 1:7]
min_max_model = MinMaxScaler()
data_rescaled = min_max_model.fit_transform(matrix)
print('{:*^60}'.format('数据标准化：归一化Min-Max'))
print(data_rescaled.round(2))

# 特征数字化：独热编码（One-Hot）
print(data.iloc[:, 7:12].head(2))
onehot_mode = OneHotEncoder(sparse=False)
data_ohe = onehot_mode.fit_transform(data.iloc[:, 7:12])
print('{:*^60}'.format('特征数字化：独热编码'))
print(data_ohe)

# 数据合并
print('{:*^60}'.format('数据维度合并：12个字段'))
data_matrix = np.hstack((data_rescaled, data_ohe))
# print(data_matrix)
# for i in data_matrix:
#     print(i.round(2))

# KMeans建模：基于平均轮廓系数，找到最佳K值(2-10)
# 关于K的取值范围：rfm用户价值(8),2-5
print('{:*^60}'.format('KMeans建模：基于平均轮廓系数'))
score_list = []
max_score = -1
for k in range(2, 6):  # 2，3，4，5
    kmeans_model = KMeans(n_clusters=k)  # 建模
    kmeans_temp = kmeans_model.fit_predict(data_matrix)  # 计算点距离
    # print(kmeans_temp)
    score = silhouette_score(data_matrix, kmeans_temp)  # 得到每个K下的平均轮廓系数
    # 获取最佳k值
    if score > max_score:  # 如果平均轮廓系数更高
        max_score = score  # 保存更高的系数值
        best_k = k  # 保存最佳的k值
        labels_temp = kmeans_temp  # 保存标签数据
    # print(k, score)
    score_list.append([k, score])  # 存每一次的k值和对应的平均轮廓系数
print('{:*^60}'.format('所有的k值以及对应平均轮廓系数'))
print(score_list)
print('最佳K值：', best_k)

# 聚类结果分析
print('{:*^60}'.format('聚类结果分析'))
# 1.合并数据与聚类标签
cluster_labels = pd.DataFrame(labels_temp, columns=['clusters'])  # 将聚类标签转化为df
merge_data = pd.concat((data, cluster_labels), axis=1)  # 整合原始数据与聚类标签
# 2.各聚类下的样本量：select count(渠道标识） from table group by 聚类标签
cluster_counts = pd.DataFrame(merge_data['渠道代号'].groupby(merge_data['clusters'])
                              .count()).T.rename({'渠道代号': 'counts'})
# 3.各聚类下的样本占比
cluster_percents = (cluster_counts / len(data)).round(3).rename({'counts': 'percentage'})
features = []
for label in range(best_k):
    label_data = merge_data[merge_data['clusters'] == label]

    # 4.数值类特征的均值
    p1_data = label_data.iloc[:, 1:7]  # 筛选出数值类特征
    p1_des = p1_data.describe().round(3)  # 获取描述性统计信息
    p1_mean = p1_des.iloc[1, :]  # 获取均值数据

    # 5.字符类特征的众数
    p2_data = label_data.iloc[:, 7:12]  # 筛选出字符类特征
    p2_des = p2_data.describe()  # 获取描述性统计信息
    p2_mode = p2_des.iloc[2, :]  # 获取频数最高的标签

    # 横向拼接2类不同特征的数据
    merge_line = pd.concat((p1_mean, p2_mode), axis=0)
    # 纵向拼接4类簇的统计数据
    features.append(merge_line)

# 6.数据合并与展示
cluster_pd = pd.DataFrame(features).T
print('{:*^60}'.format('聚类结果分析：所有信息合并'))
all_cluster_pd = pd.concat((cluster_counts, cluster_percents, cluster_pd), axis=0)
print(all_cluster_pd)
# pd.DataFrame(all_cluster_pd).to_excel('聚类结果分析.xlsx')

# 数值特征的对比分析：绘制雷达图
# 1.获取各簇/类/集群的数值特征均值、并且标准化（Max-Min归一化，0~1）
print('{:*^60}'.format('数值特征的对比分析：绘制雷达图'))
nums_data = cluster_pd.iloc[:6, :].T.astype(np.float64)  # 获取数据并转换为浮点数
nums_min_max = min_max_model.fit_transform(nums_data)  # 获取标准化（归一化）后的数据
print(nums_min_max.round(4))

# 2.绘制画布、准备数据：x轴角度、y轴数据、类别对应颜色
fig = plt.figure()  # 创建一个画布
ax = fig.add_subplot(111, polar=True)  # 创建子网格：正中央、极坐标系
angles = np.linspace(0, 2 * np.pi, 6, endpoint=False)  # 计算角度
angles = np.concatenate((angles, [angles[0]]))  # 完成了对于x轴的设置,并且最后一个值=第一个值，以闭合图形
colors = ['b', 'y', 'r', 'g']
labels = p1_data.columns.tolist()
# 3.绘制各簇对应的点线图
# y轴的设置：0 1 2 3
for i in range(len(nums_min_max)):
    temp_list = nums_min_max[i]  # 获得对应簇数值特征数据
    temp = np.concatenate((temp_list, [temp_list[0]]))  # 完成闭合
    ax.plot(angles, temp, 'o-', color=colors[i], label=i)

# 4.添加说明标签、显示雷达图
ax.set_thetagrids(angles * 180 / np.pi, labels)  # 设置极坐标
ax.set_rlim(-0.2, 1.2)  # 设置半径刻度
plt.title("数值特征对比分析")  # 设置标题
plt.legend()  # 类说明标签
plt.show()
