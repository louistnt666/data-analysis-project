import plotly.express as px
import pandas as pd
# 读取数据
response3 = pd.read_excel('D:\工作\sangji_plot.xlsx', sheet_name='Sheet1')
response3['travel_path'] = response3['travel_path'].astype(str)

# 拆分路径
response3['pages'] = response3['travel_path'].str.split('/')  # 将路径拆分为列表
response3 = response3.explode('pages')  # 将列表展开为多行

# 过滤掉空路径
response3 = response3[response3['pages'] != '']

# 按页面统计访问次数
page_counts = response3.groupby('pages')['hitnumber'].sum().reset_index()

# 计算下一步访问次数
response3['next_page'] = response3.groupby('travel_path')['pages'].shift(-1)

next_page_counts = response3.groupby('next_page')['hitnumber'].sum().reset_index()
next_page_counts.rename(columns={'hitnumber': 'next_hitnumber'}, inplace=True)

page_counts = pd.merge(page_counts, next_page_counts, left_on='pages', right_on='next_page', how='left')
page_counts['next_hitnumber'] = page_counts['next_hitnumber'].fillna(0)  # 填充 NaN 为 0

# 计算流失率
page_counts['lossrate'] = (1 - page_counts['next_hitnumber'] / page_counts['hitnumber']) * 100

# 格式化流失率为百分比
page_counts['lossrate'] = page_counts['lossrate'].apply(lambda x: f'{x:.1f}%')

# 绘制漏斗图
fig = px.funnel(page_counts, x='hitnumber', y='pages', title='用户关键页面流失情况',
                color='pages',  # 根据 travel_path 设置颜色
                color_discrete_sequence=px.colors.qualitative.Pastel)  # 使用 Pastel 颜色方案

# 更新 traces
fig.update_traces(
    textinfo='value+percent initial',  # 显示访问次数和流失率
    textposition='inside',  # 文本位置
    textfont_size=5,  # 文本字体大小
    marker=dict(line=dict(color='black', width=1))
)# 设置边框颜色和宽度

# 更新布局
fig.update_layout(
    title={
        'text': "Customers Important Pages Loss Situation",
        'y': 0.95,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top',
        'font': dict(size=20, color='darkblue')  # 标题字体大小和颜色
    },
    xaxis_title="Visit Times",  # x 轴标题
    yaxis_title="Page Path",  # y 轴标题
    font=dict(size=10, color='black'),  # 全局字体大小和颜色
    showlegend=False,  # 不显示图例
    plot_bgcolor='white',  # 背景颜色
    paper_bgcolor='lightgray',  # 纸张背景颜色
    height=600,  # 增加图表高度
    margin=dict(l=100, r=50, t=100, b=100),  # 调整边距
)
fig.show()