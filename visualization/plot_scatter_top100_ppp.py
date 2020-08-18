# -*- coding:utf-8 -*- 
# author:勤奋的大眼仔
# time:2020/8/19

import pandas as pd
import matplotlib.pyplot as plt
from pylab import mpl
import os

mpl.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体
mpl.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题
data_folder = "C:\mypython\datasets\\"
os.listdir(data_folder)
os.chdir(data_folder)
data = pd.read_csv("China_2019GDP_Top100.csv", encoding='utf-8')

"""处理数据"""
data['gdp_per_capita'] = data['gdp'] * 10 ** 8 / (data['population'] * 10000)

# 将前100个城市总产值/ 总人口 作为平均线
data['total_gdp_per_capita'] = data['gdp'].sum() * 10 ** 8 / (data['population'].sum() * 10000)

# above_avg_level:人均产值是否在平均线以上
data['above_avg_level'] = data['gdp_per_capita'] > data['total_gdp_per_capita']

# x_avg,y_avg  取平均斜线上的一点，作为后面两点一线绘图用
avg = data['total_gdp_per_capita'].unique()[0]
x_avg = data['population'].max() * 1.2
y_avg = avg * x_avg / 10 ** 4

"""绘图"""
fig, ax0 = plt.subplots(1, 1, figsize=(8, 8), dpi=300)

# 高于平均指标的圆点
cond0 = data['above_avg_level'] == False
ax0.scatter(x=data[cond0]['population'], y=data[cond0]['gdp'], color='gray')

# 低于平均指标的圆点
cond1 = data['above_avg_level'] == True
ax0.scatter(x=data[cond1]['population'], y=data[cond1]['gdp'], color='black')

# 画出平均线
ax0.plot([0, x_avg], [0, y_avg], color='#EF6351', ls='-')

# ax0坐标轴设置
ax0.set(ylim=(0, 4 * 10 ** 4), xlabel="人口(万)", ylabel="GDP（亿元）")

# 打上城市文本,平均线以上为黑色，平均线以下为灰色
cond2 = cond1 & ((data['population'] > 1000) | (data['gdp'] > 10000))
for city, population, gdp in data[cond2][['city', 'population', 'gdp']].values:
    gdp = gdp
    plt.text(population + 30, gdp, city, fontdict={'size': 10})

cond3 = cond0 & (data['population'] > 1000)
for city, population, gdp in data[cond3][['city', 'population', 'gdp']].values:
    gdp = gdp
    plt.text(population + 30, gdp, city, fontdict={'size': 10, 'color': 'gray'})

# 平均线注释
plt.annotate("top100城市GDP值（亿元）/人口（万）", xy=(2800, 2800 * avg / 10000), xytext=(1800, 32000), weight="bold",
             color="#EF6351", arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="#EF6351"))
# 标题
plt.title("2019年中国城市GDP排名百强")
plt.savefig("2019城市GDP百强.png")
plt.show()
