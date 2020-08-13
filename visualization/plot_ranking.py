# -*- coding:utf-8 -*- 
# author:勤奋的大眼仔
# time:2020/8/13
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pylab import mpl

mpl.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体
mpl.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题
msg = []
data = pd.read_csv(r"C:\mypython\datasets\2019上半年中国城市GDPtop100.csv", encoding='utf-8')
data.sample()
data.columns = ['rank', 'city', 'GDP', 'pct']
data['GDP'] = data['GDP'].apply(lambda x: int(round(x, 0)))
df = data[data["rank"] <= 12]


#  排名前5的城市数据， 绘制在y轴上方，排名第五之后的城市数据，绘制在y轴下方
def func(x):
    if x <= 5:
        return 1
    else:
        return -1


df['rank_group'] = df['rank'].apply(func)
"""将排名前五 和后五位  分成两组"""
df['y_val'] = df['rank_group'] * df['GDP']
df['height'] = df['GDP'] / df['GDP'].min()
df['height'] = df['height'] * df['rank_group']
cols = ["city", 'GDP', 'height', 'y_val']
# t1 排名前五的城市数据，t2为排名第五之后
t1 = df[df['rank_group'] == 1][cols]
t2 = df[df['rank_group'] == -1][cols]

# 每个bar左边框线距离y轴的长度，x坐标值
t1_len = t1.shape[0]
wlist = t1['height'].cumsum().tolist()[:t1_len - 1]
wlist.insert(0, 0)
t1['distance'] = np.array(wlist) + t1['height'] / 2

# 每个bar宽度
t1_height_max = t1['height'].max()
# /t1_height_max
xticks = t1['height'].tolist()[:t1_len - 1]
xticks.insert(0, 0)
t1['xticks'] = np.array(xticks) * 1.2  # /t1_height_max

##排名第五之后的
# 每个bar左边框线距离y轴的长度，x坐标值
t2_len = t2.shape[0]
wlist = t2['height'].abs().cumsum().tolist()[:t2_len - 1]
wlist.insert(0, 0)
t2['distance'] = np.array(wlist) + t2['height'].abs() / 2 + 1.5

# 每个bar宽度
t2_height_max = t2['height'].abs().max()
xticks = t2['height'].abs().tolist()[:t2_len - 1]
xticks.insert(0, 0)
t2['xticks'] = np.array(xticks)  # /t1_height_max

"""按照分成的两组数据进行绘图"""
fig, ax1 = plt.subplots(1, 1, figsize=(12, 12), dpi=80, facecolor='snow', edgecolor='snow')
color_list = ['r', 'orange', 'yellowgreen', 'green', 'dodgerblue', 'blue', 'darkgoldenrod', 'darkgreen', 'darkkhaki',
              'darkmagenta', 'darkslategray', 'darkturquoise']

# 为了让每个bar显示为正方形，height与width相等
ax1.bar(t1['distance'], height=t1['height'], width=t1['height'], color=color_list[:t1_len])
ax1.set_xlim(-1, t1['height'].sum() * 1.1)
ax1.set_ylim(-t1['height'].sum() * 1.1 / 2, t1['height'].sum() * 1.1 / 2)

ax2 = ax1.twinx()
ax2.bar(t2['distance'], height=t2['height'], width=t2['height'], color=color_list[t1_len:])
ax2.set_ylim(-t1['height'].sum() * 1.1 / 2, t1['height'].sum() * 1.1 / 2)

# bar图内文本城市、GDP数值标签
for i, y in enumerate(t1['height']):
    y_city = y * 1 / 3
    city = t1["city"][i]
    x = t1['distance'][i] - 0.3
    plt.text(x, y_city, city, fontdict={'size': 16}, fontweight='medium')
    y_gdp = y_city + 0.35
    gdp = t1['GDP'][i]
    x_gdp = t1['distance'][i] - 0.6
    plt.text(x_gdp, y_gdp, gdp, fontdict={'size': 22, 'color': 'w'}, fontweight='black')

# x轴以下 bar图内文本城市、GDP数值标签
for i, y in enumerate(t2['height']):
    i = i + 5
    y_city = y * 3 / 4
    city = t2["city"][i]
    x = t2['distance'][i] - 0.3
    plt.text(x, y_city, city, fontdict={'size': 16}, fontweight='medium')
    y_gdp = y_city + 0.35
    gdp = t2['GDP'][i]
    x_gdp = x - 0.1
    plt.text(x_gdp, y_gdp, gdp, fontdict={'size': 22, 'color': 'w'}, fontweight='black')

# 用text画标题
plt.text(2.5, 3.5, "2019上半年中国城市GDP(亿元)排名", fontdict={'size': 17})

# 不显示x轴、y轴可读
for i in [ax1, ax2]:
    i.set_xticks([])
    i.set_yticks([])

plt.show()
