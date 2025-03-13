import pandas as pd

# 读取customers.csv文件
customers_df = pd.read_csv('data/customers.csv')

customers_df
# 计算缺失值数量
customers_df.isnull().sum() / len(customers_df) * 100

# 绘制国家分布的柱状图
import matplotlib.pyplot as plt

# 统计每个国家的客户数量
country_counts = customers_df['country'].value_counts()

# 创建柱状图
plt.figure(figsize=(12, 6))
plt.bar(country_counts.index, country_counts.values)

# 设置图表标题和标签
plt.title('客户国家分布')
plt.xlabel('国家')
plt.ylabel('客户数量')

# 旋转x轴标签，提高可读性
plt.xticks(rotation=45)

# 显示图表
plt.tight_layout()
plt.show()


