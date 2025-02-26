import pandas as pd
import numpy as np
import streamlit as st

# 缓存数据生成，避免重复计算
@st.cache_data
def generate_example_data(n_samples=100):
    """生成示例电商产品数据"""
    np.random.seed(42)  # 固定随机种子以获得可重复的结果
    
    # 产品名称列表
    products = [
        "iPhone 14 Pro", "华为 Mate 60", "小米 13", "三星 Galaxy S23",
        "OPPO Find X6", "vivo X90", "荣耀 Magic5", "一加 11",
        "索尼 WH-1000XM5 耳机", "戴尔 XPS 13 笔记本", "罗技 MX Master 3 鼠标",
        "Nike 跑步鞋", "Adidas 运动套装", "Lululemon 瑜伽垫",
        "三只松鼠零食礼包", "飞科剃须刀", "小米空气净化器", "戴森吸尘器"
    ]
    
    # 商店列表
    shops = ["天猫官方旗舰店", "京东自营", "苏宁易购", "拼多多优选", "当当网", "亚马逊中国"]
    
    # 类别列表
    categories = ["电子产品", "服装", "家居", "食品", "图书"]
    
    # 生成数据
    data = {
        "产品ID": [f"PROD{str(i).zfill(4)}" for i in range(1, n_samples + 1)],
        "产品名称": np.random.choice(products, n_samples),
        "价格": np.random.randint(50, 10000, n_samples),
        "评分": np.round(np.random.uniform(1, 5, n_samples), 1),
        "评论数": np.random.randint(0, 5000, n_samples),
        "商店": np.random.choice(shops, n_samples),
        "类别": np.random.choice(categories, n_samples),
        "是否促销": np.random.choice([True, False], n_samples, p=[0.3, 0.7])
    }
    
    # 转换为DataFrame
    df = pd.DataFrame(data)
    
    # 添加一些逻辑：促销商品价格打折
    df.loc[df["是否促销"], "原价"] = df.loc[df["是否促销"], "价格"] * np.random.uniform(1.1, 1.5, df["是否促销"].sum())
    df["原价"] = df["原价"].round(2)
    
    # 为非促销商品添加NaN原价
    df.loc[~df["是否促销"], "原价"] = None
    
    # 添加一些脏数据
    # 随机选择5%的价格设为负数或0
    dirty_price_idx = np.random.choice(df.index, int(n_samples * 0.05), replace=False)
    df.loc[dirty_price_idx, "价格"] = np.random.choice([-1, 0, None], len(dirty_price_idx))
    
    # 随机选择5%的评分设为超出范围的值
    dirty_rating_idx = np.random.choice(df.index, int(n_samples * 0.05), replace=False)
    df.loc[dirty_rating_idx, "评分"] = np.random.choice([0, 6, None], len(dirty_rating_idx))
    
    # 随机选择5%的数据添加重复行
    dupes_idx = np.random.choice(df.index, int(n_samples * 0.05), replace=False)
    dupes = df.loc[dupes_idx].copy()
    df = pd.concat([df, dupes], ignore_index=True)
    
    return df

def generate_text_data(n_samples=50):
    """生成示例评论文本数据"""
    np.random.seed(42)
    
    # 用户名列表
    usernames = [
        "用户A", "用户B", "用户C", "用户D", "用户E",
        "张三", "李四", "王五", "赵六", "钱七"
    ]
    
    # 产品ID列表
    product_ids = [f"PROD{str(i).zfill(4)}" for i in range(1, 11)]
    
    # 正面评论模板
    positive_templates = [
        "这个{product}真的很好用，我非常满意。{feature}很出色，推荐购买！",
        "用了一个月的{product}，{feature}超出预期，值得入手。",
        "终于买到了心仪已久的{product}，{feature}确实不错，很满意这次购物。",
        "{product}收到了，包装完好，{feature}很棒，好评！",
        "第二次购买{product}了，一如既往的好，{feature}给人惊喜。"
    ]
    
    # 负面评论模板
    negative_templates = [
        "{product}收到后发现有问题，{feature}不符合描述，很失望。",
        "这个{product}不推荐，{feature}有明显缺陷，后悔购买。",
        "用了几天{product}就坏了，{feature}完全不行，差评！",
        "{product}质量太差，{feature}远低于预期，不值这个价。",
        "对这个{product}很不满意，{feature}与宣传严重不符。"
    ]
    
    # 产品特性
    features = {
        "电子产品": ["屏幕显示", "电池续航", "处理速度", "系统流畅度", "做工"],
        "服装": ["面料质地", "做工", "款式设计", "舒适度", "尺码精准度"],
        "家居": ["材质", "设计感", "实用性", "性价比", "外观"],
        "食品": ["口感", "新鲜度", "分量", "包装", "味道"],
        "图书": ["内容质量", "印刷质量", "排版", "纸张", "装订"]
    }
    
    # 生成评论数据
    data = {
        "评论ID": [f"REV{str(i).zfill(5)}" for i in range(1, n_samples + 1)],
        "用户名": np.random.choice(usernames, n_samples),
        "产品ID": np.random.choice(product_ids, n_samples),
        "评分": np.random.randint(1, 6, n_samples),
        "日期": pd.date_range(start='2023-01-01', periods=n_samples),
    }
    
    # 生成评论文本
    texts = []
    for i in range(n_samples):
        rating = data["评分"][i]
        product = np.random.choice(["手机", "电脑", "耳机", "T恤", "裤子", "沙发", "灯具", "零食", "书籍"])
        category = np.random.choice(list(features.keys()))
        feature = np.random.choice(features[category])
        
        if rating >= 4:  # 好评
            template = np.random.choice(positive_templates)
        else:  # 差评
            template = np.random.choice(negative_templates)
        
        text = template.format(product=product, feature=feature)
        texts.append(text)
    
    data["评论内容"] = texts
    
    return pd.DataFrame(data)

def generate_time_series_data(n_days=90):
    """生成时间序列销售数据"""
    np.random.seed(42)
    
    # 生成日期范围
    date_range = pd.date_range(start='2023-01-01', periods=n_days)
    
    # 产品列表
    products = ['手机', '电脑', '耳机', '智能手表']
    
    # 基础销量
    base_sales = {
        '手机': 100,
        '电脑': 50,
        '耳机': 80,
        '智能手表': 30
    }
    
    # 生成每个产品的每日销量
    data = []
    
    for product in products:
        base = base_sales[product]
        
        # 添加周期性波动 (周末销量增加)
        weekday_effect = [0, 0, 0, 0, 0.2, 0.5, 0.3]  # 周一到周日的效应
        
        # 添加趋势 (随时间略微增长)
        trend = np.linspace(0, 0.3, n_days)
        
        # 添加季节性 (每月初销量上升)
        monthly_effect = np.sin(np.linspace(0, n_days/30*2*np.pi, n_days)) * 0.2
        
        # 添加促销效应 (随机几天有大幅增长)
        promo_days = np.random.choice(n_days, size=int(n_days*0.1), replace=False)
        promo_effect = np.zeros(n_days)
        promo_effect[promo_days] = np.random.uniform(0.5, 1.0, size=len(promo_days))
        
        # 计算最终销量
        for i, date in enumerate(date_range):
            weekday = date.weekday()
            
            # 计算当天的销量
            sales = base * (1 + weekday_effect[weekday] + trend[i] + monthly_effect[i] + promo_effect[i])
            
            # 添加随机波动
            sales = int(sales * np.random.uniform(0.9, 1.1))
            
            data.append({
                '日期': date,
                '产品': product,
                '销量': sales,
                '是否促销': bool(promo_effect[i] > 0)
            })
    
    return pd.DataFrame(data) 