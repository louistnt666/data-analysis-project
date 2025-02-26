#绘制桑基图
from collections import defaultdict
import pandas as pd

# 读取数据
response2 = pd.read_excel('D:\工作\sangji_plot.xlsx', sheet_name='Sheet1')
response2['travel_path'] = response2['travel_path'].astype(str)
# 初始化字典来存储源节点、目标节点和流量
links = defaultdict(int)

# 处理每条路径
for path in response2['travel_path']:
    if pd.notna(path) and path != 'nan' and path.strip() != '':  #处理现有的数据中包含多个页面，将其拆分
        nodes = path.split('/')
        for i in range(len(nodes) - 1):
            source = nodes[i].strip()  # 去除空白字符
            target = nodes[i + 1].strip()
            links[(source, target)] += 1

# 转换为桑基图所需的格式
sources = []
targets = []
values = []

for (source, target), value in links.items():
    sources.append(source)
    targets.append(target)
    values.append(value)

# 获取所有唯一节点
all_nodes = list(set(sources + targets))

import plotly.graph_objects as go

# 创建桑基图
fig = go.Figure(data=[go.Sankey(
    node=dict(
        pad=15,
        thickness=20,
        line=dict(color="black", width=0.5),
        label=list(set(sources + targets)),
        color="blue",
        hoverinfo="all"
    ),
    link=dict(
        source=[all_nodes.index(source) for source in sources],  # 源节点索引
        target=[all_nodes.index(target) for target in targets],  # 目标节点索引
        value=values,  # 流量值
        color="rgba(0, 128, 255, 0.5)",
        hoverinfo="all"
    )
)])

# 设置布局
fig.update_layout(
    title="Sankey Diagram",  # 标题
    font=dict(size=12, color="black"),  # 字体样式
    width=800,  # 宽度
    height=600,  # 高度
    plot_bgcolor="white",  # 图表背景颜色
    paper_bgcolor="white"  # 画布背景颜色
)

# 显示图表
fig.show()
