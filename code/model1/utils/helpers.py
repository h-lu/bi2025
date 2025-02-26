import pandas as pd
import numpy as np
import re
import random
from bs4 import BeautifulSoup
import streamlit as st
import os

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

def load_html_file(file_path):
    """加载HTML文件并返回BeautifulSoup对象"""
    # 获取当前文件的绝对路径
    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    full_path = os.path.join(current_dir, file_path)
    
    try:
        with open(full_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
        return html_content, BeautifulSoup(html_content, 'html.parser')
    except Exception as e:
        st.error(f"无法加载HTML文件: {e}")
        return None, None

def extract_product_data(soup):
    """从BeautifulSoup对象中提取产品信息"""
    products = []
    product_elements = soup.select('.product')
    
    for product in product_elements:
        product_id = product.get('id', '')
        title = product.select_one('.product-title').text.strip() if product.select_one('.product-title') else 'Unknown'
        
        # 价格处理
        price_elem = product.select_one('.price')
        price = None
        original_price = None
        if price_elem:
            price_text = price_elem.get_text().strip()
            price_match = re.search(r'¥(\d+(?:\.\d+)?)', price_text)
            price = float(price_match.group(1)) if price_match else None
            
            # 原价
            original_price_elem = product.select_one('.original-price')
            if original_price_elem:
                op_match = re.search(r'¥(\d+(?:\.\d+)?)', original_price_elem.text)
                original_price = float(op_match.group(1)) if op_match else None
        
        # 评分处理
        rating_elem = product.select_one('.rating')
        rating = None
        if rating_elem:
            score_elem = rating_elem.select_one('.score')
            if score_elem:
                rating = float(score_elem.text.strip())
        
        # 评论数处理
        reviews_elem = product.select_one('.reviews')
        reviews = 0
        if reviews_elem:
            reviews_match = re.search(r'评论数: (\d+)', reviews_elem.text)
            reviews = int(reviews_match.group(1)) if reviews_match else 0
        
        # 商店信息
        shop_elem = product.select_one('.shop')
        shop = shop_elem.text.strip() if shop_elem else 'Unknown'
        
        # 类别
        category_elem = product.select_one('.category')
        category = category_elem.text.strip() if category_elem else 'Unknown'
        
        # 是否促销
        is_promo = bool(product.select_one('.promotion'))
        
        products.append({
            'product_id': product_id,
            'title': title,
            'price': price,
            'original_price': original_price,
            'rating': rating,
            'reviews': reviews,
            'shop': shop,
            'category': category,
            'is_promotion': is_promo
        })
    
    return products

def extract_review_data(soup):
    """从BeautifulSoup对象中提取评论信息"""
    reviews = []
    review_elements = soup.select('.review')
    
    for review in review_elements:
        review_id = review.get('id', '')
        
        # 用户名
        user_name_elem = review.select_one('.user-name')
        user_name = user_name_elem.text.strip() if user_name_elem else 'Unknown'
        
        # 评论日期
        review_date_elem = review.select_one('.review-date')
        review_date = review_date_elem.text.strip() if review_date_elem else 'Unknown'
        
        # 评分
        rating_elem = review.select_one('.review-rating')
        rating = 0
        if rating_elem:
            stars = rating_elem.text.count('★')
            rating = stars
        
        # 评论内容
        content_elem = review.select_one('.review-content')
        content = content_elem.text.strip() if content_elem else ''
        
        # 评论图片
        has_photos = bool(review.select('.review-photo'))
        
        reviews.append({
            'review_id': review_id,
            'user_name': user_name,
            'date': review_date,
            'rating': rating,
            'content': content,
            'has_photos': has_photos
        })
    
    return reviews

def sentiment_analysis(text):
    """简单的情感分析，返回积极/消极分数"""
    # 这是一个非常简化的情感分析，实际情况应使用NLP模型
    positive_words = ['好', '棒', '喜欢', '满意', '推荐', '优秀', '惊艳', '不错', '强', '出色', 
                     '清晰', '流畅', '稳定', '值得', '爱上', '优质', '高级', '超出预期']
    negative_words = ['差', '失望', '不满', '问题', '糟', '坏', '后悔', '慢', '贵', '不值', 
                     '不推荐', '不好', '一般', '中规中矩', '卡顿', '发热']
    
    positive_score = sum(1 for word in positive_words if word in text)
    negative_score = sum(1 for word in negative_words if word in text)
    
    # 计算总分，范围从-1到1
    total_words = len(text)
    if total_words > 0:
        score = (positive_score - negative_score) / (positive_score + negative_score) if (positive_score + negative_score) > 0 else 0
    else:
        score = 0
    
    # 返回情感标签和分数
    if score > 0.2:
        return "积极", score
    elif score < -0.2:
        return "消极", score
    else:
        return "中性", score 