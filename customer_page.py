#计算跳转概率矩阵
import pandas as pd
from collections import defaultdict
# 按用户和访问分组，构建路径
# 读取数据
response3 = pd.read_excel('D:\工作\sangji_plot.xlsx', sheet_name='Sheet1')
response3['travel_path'] = response3['travel_path'].astype(str)

# 拆分路径
response3['pages'] = response3['travel_path'].str.split('/')  # 将路径拆分为列表
response3 = response3.explode('pages')  # 将列表展开为多行

# 过滤掉空路径
response3 = response3[response3['pages'] != '']
response3_sorted = response3.sort_values(by=['fullVisitorId', 'visitId', 'hitnumber'])
paths = response3_sorted.groupby(['fullVisitorId', 'visitId'])['pages'].apply(list)

# 生成页面跳转对
transition_counts = defaultdict(int)  # 存储跳转次数
for path in paths:
    for i in range(len(path) - 1):
        current_page = path[i]
        next_page = path[i + 1]
        transition_counts[(current_page, next_page)] += 1

# 构建跳转次数矩阵
unique_pages = response3['pages'].unique()
transition_matrix = pd.DataFrame(0, index=unique_pages, columns=unique_pages)
for (current, next), count in transition_counts.items():
    transition_matrix.loc[current, next] = count
# 计算跳转概率矩阵
transition_prob_matrix = transition_matrix.div(transition_matrix.sum(axis=1), axis=0)
print("\n跳转概率矩阵：")
print(transition_prob_matrix)

# 将跳转概率矩阵保存为 .xlsx 文件
output_file = 'transition_prob_matrix.xlsx'
transition_prob_matrix.to_excel(output_file, sheet_name='跳转概率矩阵')

#计算高频路径
import matplotlib.pyplot as plt
import plotly.express as px
paths = response3.groupby(['fullVisitorId', 'visitId'])['pages'].apply(list)
# 统计高频路径
from collections import Counter
path_counter = Counter(paths.apply(tuple))  # 将路径转换为元组以便统计
top_paths = path_counter.most_common(10)  # 取前 10 条高频路径
print('高频路径：', top_paths)