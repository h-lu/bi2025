import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import os
from faker import Faker
import matplotlib.pyplot as plt
import seaborn as sns

# 设置随机种子以确保可重复性
np.random.seed(42)
random.seed(42)
fake = Faker()
Faker.seed(42)

# 创建输出目录
if not os.path.exists('data'):
    os.makedirs('data')

# 定义常量
START_DATE = datetime(2022, 1, 1)
END_DATE = datetime(2023, 12, 31)
NUM_CUSTOMERS = 5000
NUM_PRODUCTS = 500
NUM_TRANSACTIONS = 100000
NUM_MARKETING_CAMPAIGNS = 50

# 地区和国家
REGIONS = {
    'North America': ['USA', 'Canada', 'Mexico'],
    'Europe': ['UK', 'Germany', 'France', 'Italy', 'Spain', 'Netherlands'],
    'Asia Pacific': ['China', 'Japan', 'South Korea', 'Australia', 'India', 'Singapore'],
    'Latin America': ['Brazil', 'Argentina', 'Colombia', 'Chile'],
    'Middle East & Africa': ['UAE', 'South Africa', 'Egypt', 'Saudi Arabia']
}

# 产品类别和子类别
PRODUCT_CATEGORIES = {
    'Electronics': ['Smartphones', 'Laptops', 'Tablets', 'Cameras', 'Audio', 'Accessories'],
    'Fashion': ['Men\'s Clothing', 'Women\'s Clothing', 'Footwear', 'Accessories', 'Jewelry'],
    'Home & Kitchen': ['Furniture', 'Appliances', 'Kitchenware', 'Decor', 'Bedding'],
    'Beauty & Personal Care': ['Skincare', 'Makeup', 'Haircare', 'Fragrance', 'Personal Hygiene'],
    'Sports & Outdoors': ['Fitness Equipment', 'Outdoor Gear', 'Sports Apparel', 'Camping', 'Water Sports'],
    'Books & Media': ['Fiction', 'Non-fiction', 'E-books', 'Movies', 'Music'],
    'Toys & Games': ['Board Games', 'Toys', 'Video Games', 'Puzzles', 'Collectibles']
}

# 营销渠道
MARKETING_CHANNELS = ['Email', 'Social Media', 'Search Engine', 'Display Ads', 'Affiliate', 'Direct Mail', 'TV', 'Radio']

# 支付方式
PAYMENT_METHODS = ['Credit Card', 'Debit Card', 'PayPal', 'Apple Pay', 'Google Pay', 'Bank Transfer', 'Gift Card']

# 客户类型
CUSTOMER_SEGMENTS = ['New', 'Returning', 'Loyal', 'VIP', 'At Risk', 'Dormant']

# 设备类型
DEVICE_TYPES = ['Desktop', 'Mobile', 'Tablet', 'App']

# 生成客户数据
def generate_customer_data():
    customers = []
    
    for i in range(1, NUM_CUSTOMERS + 1):
        region = random.choice(list(REGIONS.keys()))
        country = random.choice(REGIONS[region])
        
        # 故意引入一些数据问题
        if i % 50 == 0:  # 每50个客户有一个缺失年龄
            age = np.nan
        else:
            age = random.randint(18, 75)
            
        if i % 30 == 0:  # 每30个客户有一个异常年龄
            age = random.randint(100, 120)
        
        # 收入数据有一些异常值和不同格式
        if i % 100 == 0:
            income = f"${random.randint(20, 200)}K"  # 字符串格式
        elif i % 75 == 0:
            income = random.randint(1000000, 2000000)  # 异常高值
        else:
            income = random.randint(20000, 200000)
        
        # 注册日期
        days_before_end = random.randint(0, (END_DATE - START_DATE).days)
        registration_date = END_DATE - timedelta(days=days_before_end)
        
        # 有时邮箱格式不正确
        if i % 80 == 0:
            email = fake.name().replace(' ', '') + "at" + random.choice(["gmail", "yahoo", "hotmail"]) + ".com"
        else:
            email = fake.email()
        
        # 客户细分
        segment_weights = [0.3, 0.3, 0.2, 0.1, 0.05, 0.05]  # 不同细分的概率
        segment = np.random.choice(CUSTOMER_SEGMENTS, p=segment_weights)
        
        # 有时会有重复的客户ID（数据问题）
        customer_id = f"CUST{i:05d}" if i % 200 != 0 else f"CUST{i-1:05d}"
        
        customers.append({
            'customer_id': customer_id,
            'name': fake.name(),
            'email': email,
            'age': age,
            'gender': random.choice(['Male', 'Female', 'Other', None]),
            'region': region,
            'country': country,
            'city': fake.city(),
            'income': income,
            'registration_date': registration_date.strftime('%Y-%m-%d'),
            'segment': segment,
            'preferred_payment': random.choice(PAYMENT_METHODS),
            'preferred_device': random.choice(DEVICE_TYPES),
            'total_purchases': random.randint(1, 100),
            'newsletter_subscription': random.choice([True, False]),
            'loyalty_points': random.randint(0, 10000)
        })
    
    return pd.DataFrame(customers)

# 生成产品数据
def generate_product_data():
    products = []
    
    for i in range(1, NUM_PRODUCTS + 1):
        category = random.choice(list(PRODUCT_CATEGORIES.keys()))
        subcategory = random.choice(PRODUCT_CATEGORIES[category])
        
        # 基础价格
        base_price = round(random.uniform(10, 1000), 2)
        
        # 一些产品有折扣
        if random.random() < 0.3:
            discount_rate = round(random.uniform(0.05, 0.5), 2)
        else:
            discount_rate = 0
            
        # 一些产品有缺货问题
        if random.random() < 0.1:
            stock_status = 'Out of Stock'
            stock_quantity = 0
        else:
            stock_status = 'In Stock'
            stock_quantity = random.randint(1, 1000)
        
        # 一些产品有评分缺失
        if random.random() < 0.05:
            rating = np.nan
        else:
            rating = round(random.uniform(1, 5), 1)
        
        # 产品ID有时格式不一致
        if i % 50 == 0:
            product_id = str(i)  # 纯数字ID
        else:
            product_id = f"PROD{i:05d}"  # 标准格式
        
        products.append({
            'product_id': product_id,
            'name': f"{subcategory} Item {i}",
            'category': category,
            'subcategory': subcategory,
            'base_price': base_price,
            'discount_rate': discount_rate,
            'current_price': round(base_price * (1 - discount_rate), 2),
            'stock_quantity': stock_quantity,
            'stock_status': stock_status,
            'rating': rating,
            'num_reviews': random.randint(0, 1000),
            'supplier': fake.company(),
            'weight_kg': round(random.uniform(0.1, 20), 2) if random.random() > 0.1 else np.nan,
            'launch_date': (START_DATE - timedelta(days=random.randint(0, 1000))).strftime('%Y-%m-%d'),
            'is_bestseller': random.random() < 0.1
        })
    
    return pd.DataFrame(products)

# 生成交易数据
def generate_transaction_data(customers_df, products_df):
    transactions = []
    
    # 获取所有客户ID和产品ID
    customer_ids = customers_df['customer_id'].unique()
    product_ids = products_df['product_id'].unique()
    
    # 生成交易
    for i in range(1, NUM_TRANSACTIONS + 1):
        # 交易日期
        days_from_start = random.randint(0, (END_DATE - START_DATE).days)
        transaction_date = START_DATE + timedelta(days=days_from_start)
        
        # 选择客户
        customer_id = random.choice(customer_ids)
        
        # 交易中的产品数量
        num_products_in_transaction = random.choices([1, 2, 3, 4, 5], weights=[0.5, 0.25, 0.15, 0.07, 0.03])[0]
        
        # 为交易选择产品
        transaction_products = random.sample(list(product_ids), num_products_in_transaction)
        
        # 交易ID有时格式不一致
        if i % 100 == 0:
            transaction_id = str(i * 1000)  # 不一致的ID格式
        else:
            transaction_id = f"TRX{i:06d}"  # 标准格式
        
        # 有时交易状态不一致
        if random.random() < 0.05:
            status = random.choice(['Cancelled', 'Refunded', 'Failed'])
        else:
            status = 'Completed'
        
        # 基本交易信息
        base_transaction = {
            'transaction_id': transaction_id,
            'customer_id': customer_id,
            'date': transaction_date.strftime('%Y-%m-%d'),
            'time': transaction_date.strftime('%H:%M:%S'),
            'payment_method': random.choice(PAYMENT_METHODS),
            'status': status,
            'device': random.choice(DEVICE_TYPES),
            'coupon_used': random.random() < 0.2,
            'shipping_cost': round(random.uniform(0, 20), 2),
            'tax_amount': None,  # 将在后面计算
            'total_amount': None,  # 将在后面计算
        }
        
        # 为每个产品创建一个交易项
        subtotal = 0
        for product_id in transaction_products:
            product = products_df[products_df['product_id'] == product_id].iloc[0]
            quantity = random.randint(1, 5)
            price = product['current_price']
            item_total = price * quantity
            subtotal += item_total
            
            transaction_item = base_transaction.copy()
            transaction_item['product_id'] = product_id
            transaction_item['product_category'] = product['category']
            transaction_item['product_subcategory'] = product['subcategory']
            transaction_item['quantity'] = quantity
            transaction_item['unit_price'] = price
            transaction_item['item_total'] = item_total
            
            # 计算税和总额
            tax_rate = round(random.uniform(0.05, 0.2), 2)
            tax_amount = round(item_total * tax_rate, 2)
            total_amount = item_total + tax_amount + transaction_item['shipping_cost']
            
            transaction_item['tax_amount'] = tax_amount
            transaction_item['total_amount'] = total_amount
            
            # 添加一些数据问题
            if random.random() < 0.02:  # 2%的交易有日期格式问题
                transaction_item['date'] = transaction_date.strftime('%d/%m/%Y')
            
            if random.random() < 0.01:  # 1%的交易有价格为负数
                transaction_item['unit_price'] = -price
                transaction_item['item_total'] = -item_total
            
            transactions.append(transaction_item)
    
    return pd.DataFrame(transactions)

# 生成营销活动数据
def generate_marketing_data():
    marketing_campaigns = []
    
    for i in range(1, NUM_MARKETING_CAMPAIGNS + 1):
        # 活动开始和结束日期
        start_days_from_start = random.randint(0, (END_DATE - START_DATE).days - 30)
        campaign_start = START_DATE + timedelta(days=start_days_from_start)
        campaign_end = campaign_start + timedelta(days=random.randint(7, 90))
        
        # 确保结束日期不超过总时间范围
        if campaign_end > END_DATE:
            campaign_end = END_DATE
        
        # 目标区域和产品类别
        target_region = random.choice(list(REGIONS.keys()))
        target_category = random.choice(list(PRODUCT_CATEGORIES.keys()))
        
        # 预算和支出
        budget = round(random.uniform(5000, 100000), 2)
        
        # 有时支出超过预算（数据问题）
        if random.random() < 0.1:
            spend = round(budget * random.uniform(1.0, 1.2), 2)
        else:
            spend = round(budget * random.uniform(0.8, 1.0), 2)
        
        # 活动效果指标
        impressions = random.randint(10000, 1000000)
        clicks = random.randint(1000, min(100000, impressions))
        conversions = random.randint(10, min(10000, clicks))
        
        # 计算派生指标
        ctr = round(clicks / impressions, 4) if impressions > 0 else 0
        conversion_rate = round(conversions / clicks, 4) if clicks > 0 else 0
        cpa = round(spend / conversions, 2) if conversions > 0 else np.nan
        roi = round((conversions * random.uniform(50, 200) - spend) / spend, 2) if spend > 0 else np.nan
        
        # 有时ROI数据缺失或格式不一致
        if random.random() < 0.05:
            roi = np.nan
        elif random.random() < 0.05:
            roi = f"{int(roi * 100)}%"  # 字符串格式
        
        marketing_campaigns.append({
            'campaign_id': f"CAM{i:03d}",
            'name': f"{target_category} {random.choice(['Promotion', 'Sale', 'Launch', 'Awareness'])} {i}",
            'channel': random.choice(MARKETING_CHANNELS),
            'start_date': campaign_start.strftime('%Y-%m-%d'),
            'end_date': campaign_end.strftime('%Y-%m-%d'),
            'target_region': target_region,
            'target_category': target_category,
            'target_audience': random.choice(['New Customers', 'Existing Customers', 'All']),
            'budget': budget,
            'spend': spend,
            'impressions': impressions,
            'clicks': clicks,
            'conversions': conversions,
            'ctr': ctr,
            'conversion_rate': conversion_rate,
            'cpa': cpa,
            'roi': roi,
            'objective': random.choice(['Brand Awareness', 'Lead Generation', 'Sales', 'Customer Retention']),
            'notes': fake.text(max_nb_chars=100) if random.random() < 0.3 else None
        })
    
    return pd.DataFrame(marketing_campaigns)

# 生成网站流量数据
def generate_website_traffic_data():
    traffic_data = []
    
    current_date = START_DATE
    while current_date <= END_DATE:
        # 基础流量，有季节性趋势
        base_traffic = 5000 + 2000 * np.sin(2 * np.pi * current_date.timetuple().tm_yday / 365)
        
        # 周末流量增加
        if current_date.weekday() >= 5:  # 5和6是周六和周日
            base_traffic *= 1.3
        
        # 假日流量激增
        holidays = [
            datetime(current_date.year, 1, 1),   # 新年
            datetime(current_date.year, 2, 14),  # 情人节
            datetime(current_date.year, 11, 11), # 双十一
            datetime(current_date.year, 11, 27), # 黑色星期五（假设在11月第四个星期五）
            datetime(current_date.year, 12, 25)  # 圣诞节
        ]
        
        if any(holiday.month == current_date.month and holiday.day == current_date.day for holiday in holidays):
            base_traffic *= random.uniform(1.5, 2.5)
        
        # 添加随机波动
        daily_traffic = int(base_traffic * random.uniform(0.8, 1.2))
        
        # 计算各渠道流量
        organic_search = int(daily_traffic * random.uniform(0.3, 0.5))
        paid_search = int(daily_traffic * random.uniform(0.1, 0.25))
        social_media = int(daily_traffic * random.uniform(0.1, 0.2))
        email = int(daily_traffic * random.uniform(0.05, 0.15))
        direct = int(daily_traffic * random.uniform(0.1, 0.2))
        referral = daily_traffic - (organic_search + paid_search + social_media + email + direct)
        
        # 计算转化率和跳出率
        conversion_rate = round(random.uniform(0.01, 0.05), 4)
        bounce_rate = round(random.uniform(0.2, 0.6), 4)
        
        # 有时数据缺失（数据问题）
        if random.random() < 0.02:
            organic_search = np.nan
            paid_search = np.nan
        
        traffic_data.append({
            'date': current_date.strftime('%Y-%m-%d'),
            'total_visits': daily_traffic,
            'organic_search': organic_search,
            'paid_search': paid_search,
            'social_media': social_media,
            'email': email,
            'direct': direct,
            'referral': referral,
            'new_visitors_pct': round(random.uniform(0.3, 0.7), 2),
            'returning_visitors_pct': None,  # 将在后面计算
            'pages_per_session': round(random.uniform(2, 8), 2),
            'avg_session_duration': round(random.uniform(60, 600), 2),
            'conversion_rate': conversion_rate,
            'bounce_rate': bounce_rate
        })
        
        current_date += timedelta(days=1)
    
    traffic_df = pd.DataFrame(traffic_data)
    
    # 计算派生字段
    traffic_df['returning_visitors_pct'] = 1 - traffic_df['new_visitors_pct']
    
    return traffic_df

# 生成所有数据集
def generate_all_datasets():
    print("生成客户数据...")
    customers_df = generate_customer_data()
    
    print("生成产品数据...")
    products_df = generate_product_data()
    
    print("生成交易数据...")
    transactions_df = generate_transaction_data(customers_df, products_df)
    
    print("生成营销活动数据...")
    marketing_df = generate_marketing_data()
    
    print("生成网站流量数据...")
    traffic_df = generate_website_traffic_data()
    
    # 保存数据集
    customers_df.to_csv('data/customers.csv', index=False)
    products_df.to_csv('data/products.csv', index=False)
    transactions_df.to_csv('data/transactions.csv', index=False)
    marketing_df.to_csv('data/marketing_campaigns.csv', index=False)
    traffic_df.to_csv('data/website_traffic.csv', index=False)
    
    print("所有数据集已生成并保存到 'data' 目录")
    
    # 生成数据概览
    print("\n数据集概览:")
    print(f"客户数据: {customers_df.shape[0]} 行, {customers_df.shape[1]} 列")
    print(f"产品数据: {products_df.shape[0]} 行, {products_df.shape[1]} 列")
    print(f"交易数据: {transactions_df.shape[0]} 行, {transactions_df.shape[1]} 列")
    print(f"营销活动数据: {marketing_df.shape[0]} 行, {marketing_df.shape[1]} 列")
    print(f"网站流量数据: {traffic_df.shape[0]} 行, {traffic_df.shape[1]} 列")
    
    # 生成一些示例图表
    plt.figure(figsize=(12, 6))
    
    # 按类别统计产品数量
    plt.subplot(1, 2, 1)
    category_counts = products_df['category'].value_counts()
    sns.barplot(x=category_counts.index, y=category_counts.values)
    plt.title('产品类别分布')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    # 按月份统计交易数量
    plt.subplot(1, 2, 2)
    transactions_df['month'] = pd.to_datetime(transactions_df['date']).dt.strftime('%Y-%m')
    monthly_transactions = transactions_df.groupby('month').size()
    sns.lineplot(x=monthly_transactions.index, y=monthly_transactions.values)
    plt.title('月度交易量')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    plt.savefig('data/sample_charts.png')
    print("示例图表已保存到 'data/sample_charts.png'")
    
    return customers_df, products_df, transactions_df, marketing_df, traffic_df

if __name__ == "__main__":
    generate_all_datasets() 