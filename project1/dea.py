from matplotlib import pyplot as plt
import pandas as pd

# 读取customers.csv文件
customers_df = pd.read_csv('data/customers.csv')

# 计算不同性别的用户数
gender_counts = customers_df['gender'].value_counts()
print(gender_counts)

# 绘制柱状图
# 设置现代化的图表样式
# 设置Mac系统下的中文字体
plt.rcParams['font.sans-serif'] = ['PingFang HK', 'Arial Unicode MS']  # Mac系统下的中文字体
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

plt.style.use('seaborn')

# 创建图形和轴对象
fig, ax = plt.subplots(figsize=(10, 6))

# 绘制柱状图
bars = gender_counts.plot(kind='bar', ax=ax, color=['#2ecc71', '#3498db'])

# 美化图表
plt.title('性别分布', fontsize=14, pad=15)
plt.xlabel('性别', fontsize=12)
plt.ylabel('数量', fontsize=12)

# 添加数值标签
for i, v in enumerate(gender_counts):
    ax.text(i, v, str(v), ha='center', va='bottom')

# 调整布局
plt.tight_layout()

# 显示图表
plt.show()


# 计算不同国家的用户数
country_counts = customers_df['country'].value_counts()
print(country_counts)

# 定义各大洲及其包含的国家
continents = {
    'Asia': ['China', 'Japan', 'South Korea', 'India'],
    'Europe': ['UK', 'France', 'Germany', 'Italy', 'Spain'],
    'North America': ['USA', 'Canada', 'Mexico'],
    'South America': ['Brazil', 'Argentina', 'Chile'],
    'Oceania': ['Australia', 'New Zealand'],
    'Africa': ['South Africa', 'Egypt', 'Nigeria']
}

# 定义各大洲对应的颜色
continent_colors = {
    'Asia': '#e74c3c',      # 红色
    'Europe': '#3498db',    # 蓝色
    'North America': '#2ecc71',  # 绿色
    'South America': '#f1c40f',  # 黄色
    'Oceania': '#9b59b6',   # 紫色
    'Africa': '#e67e22'     # 橙色
}

# 为每个国家分配对应大洲的颜色
country_colors = []
for country in country_counts.index:
    color_assigned = False
    for continent, countries in continents.items():
        if country in countries:
            country_colors.append(continent_colors[continent])
            color_assigned = True
            break
    if not color_assigned:
        country_colors.append('#95a5a6')  # 默认灰色用于未分类国家

# 绘制柱状图
# 创建图形和轴对象
fig, ax = plt.subplots(figsize=(12, 6))

# 绘制柱状图
bars = country_counts.plot(kind='bar', ax=ax, color=country_colors)

# 美化图表
plt.title('用户国家分布', fontsize=14, pad=15)
plt.xlabel('国家', fontsize=12)
plt.ylabel('数量', fontsize=12)

# 添加数值标签
for i, v in enumerate(country_counts):
    ax.text(i, v, str(v), ha='center', va='bottom')

# 由于国家名称可能较长，旋转x轴标签以防重叠
plt.xticks(rotation=45, ha='right')

# 调整布局
plt.tight_layout()

# 显示图表
plt.show()
