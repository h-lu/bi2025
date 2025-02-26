import re
from bs4 import BeautifulSoup
import os
import streamlit as st

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

def extract_news_data(soup):
    """从BeautifulSoup对象中提取新闻信息"""
    news_items = []
    article_elements = soup.select('article.news-item')
    
    for article in article_elements:
        article_id = article.get('id', '')
        
        # 标题
        title_elem = article.select_one('h2.news-title')
        title = title_elem.text.strip() if title_elem else 'Unknown'
        
        # 发布日期
        date_elem = article.select_one('.news-date')
        date = date_elem.text.strip() if date_elem else 'Unknown'
        
        # 摘要
        summary_elem = article.select_one('.news-summary')
        summary = summary_elem.text.strip() if summary_elem else ''
        
        # 作者
        author_elem = article.select_one('.news-author')
        author = author_elem.text.strip() if author_elem else 'Unknown'
        
        # 类别
        category_elem = article.select_one('.news-category')
        category = category_elem.text.strip() if category_elem else 'Unknown'
        
        # 链接
        link_elem = article.select_one('a.news-link')
        link = link_elem.get('href', '#') if link_elem else '#'
        
        news_items.append({
            'article_id': article_id,
            'title': title,
            'date': date,
            'summary': summary,
            'author': author,
            'category': category,
            'link': link
        })
    
    return news_items

def parse_api_json(json_data):
    """解析API返回的JSON数据"""
    try:
        # 提取主要数据
        if 'data' in json_data:
            items = json_data['data'].get('items', [])
            return items
        elif 'results' in json_data:
            return json_data['results']
        else:
            return json_data
    except Exception as e:
        st.error(f"解析JSON数据时出错: {e}")
        return [] 