import streamlit as st
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import os
import sys

# 添加项目根目录到Python路径，以便导入utils模块
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.helpers import load_html_file, extract_product_data

def show():
    """显示网络爬虫基础页面内容"""
    st.header("网络爬虫基础")
    
    st.markdown("""
    ## 网络爬虫概述
    
    网络爬虫（Web Scraping）是一种自动从网页中提取数据的技术。爬虫程序模拟浏览器行为，访问网页，提取需要的信息，并将其转换为结构化数据。
    """)
    
    # HTTP基础知识
    st.subheader("HTTP基础知识")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### HTTP请求方法
        
        - **GET**: 用于获取数据，参数附加在URL上
        - **POST**: 用于提交数据，参数在请求体中
        - **PUT**: 用于更新资源
        - **DELETE**: 用于删除资源
        - **HEAD**: 类似GET但只获取头信息
        
        大多数爬虫操作使用GET方法。
        """)
        
        st.markdown("""
        ### 常见状态码
        
        - **200 OK**: 请求成功
        - **301/302**: 重定向
        - **403 Forbidden**: 服务器拒绝请求
        - **404 Not Found**: 资源不存在
        - **429 Too Many Requests**: 请求过于频繁
        - **500 Server Error**: 服务器内部错误
        """)
    
    with col2:
        st.markdown("""
        ### HTTP头部信息
        
        重要的请求头:
        - **User-Agent**: 标识客户端类型
        - **Accept**: 指定接受的内容类型
        - **Referer**: 来源页面URL
        - **Cookie**: 保存会话信息
        
        重要的响应头:
        - **Content-Type**: 返回内容的类型
        - **Content-Length**: 内容长度
        - **Set-Cookie**: 设置Cookie
        """)
        
        st.markdown("""
        ### 常见爬虫障碍
        
        - **robots.txt**: 网站对爬虫的规则说明
        - **验证码**: CAPTCHA等机制
        - **IP限制**: 基于IP的访问限制
        - **用户代理检测**: 检测是否是浏览器
        - **JavaScript渲染**: 内容通过JS动态加载
        """)
    
    # Requests库使用
    st.subheader("使用Requests库发送HTTP请求")
    
    with st.expander("Requests库基本使用"):
        st.code("""
import requests

# 简单的GET请求
response = requests.get('https://example.com')
print(f"状态码: {response.status_code}")
print(f"内容类型: {response.headers['Content-Type']}")

# 打印返回的内容
print(response.text[:500])  # 打印前500个字符

# 带参数的GET请求
params = {
    'q': 'python web scraping',
    'page': 1
}
response = requests.get('https://example.com/search', params=params)
print(f"完整URL: {response.url}")

# 自定义头部信息
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
}
response = requests.get('https://example.com', headers=headers)

# 处理响应内容
if response.status_code == 200:
    # 文本内容
    html_content = response.text
    
    # JSON响应
    if 'application/json' in response.headers.get('Content-Type', ''):
        data = response.json()
        print(data)
else:
    print(f"请求失败: {response.status_code}")
    print(response.text)

# 处理超时和异常
try:
    response = requests.get('https://example.com', timeout=5)
    response.raise_for_status()  # 如果状态码不是200系列，抛出异常
except requests.exceptions.Timeout:
    print("请求超时")
except requests.exceptions.HTTPError as e:
    print(f"HTTP错误: {e}")
except requests.exceptions.RequestException as e:
    print(f"请求异常: {e}")
        """, language="python")
    
    # BeautifulSoup基础
    st.subheader("使用BeautifulSoup解析HTML")
    
    with st.expander("BeautifulSoup基本使用"):
        st.code("""
from bs4 import BeautifulSoup

# HTML字符串
html = '''
<!DOCTYPE html>
<html>
<head>
    <title>产品列表</title>
</head>
<body>
    <h1>热门产品</h1>
    <div class="products">
        <div class="product" id="p1">
            <h2 class="name">笔记本电脑</h2>
            <p class="price">¥5999</p>
            <p class="description">高性能商务本，16GB内存，512GB SSD</p>
            <div class="rating">评分: 4.7</div>
        </div>
        <div class="product" id="p2">
            <h2 class="name">智能手机</h2>
            <p class="price">¥3999</p>
            <p class="description">旗舰拍照手机，8GB内存，256GB存储</p>
            <div class="rating">评分: 4.5</div>
        </div>
    </div>
</body>
</html>
'''

# 创建BeautifulSoup对象
soup = BeautifulSoup(html, 'html.parser')

# 1. 查找单个元素
title = soup.title
print(f"标题: {title.text}")

first_product = soup.find('div', class_='product')
print(f"第一个产品ID: {first_product['id']}")

# 2. 查找所有匹配元素
all_products = soup.find_all('div', class_='product')
print(f"找到{len(all_products)}个产品")

# 3. CSS选择器
# 选择所有产品名称
product_names = soup.select('.product .name')
for name in product_names:
    print(f"产品名称: {name.text}")

# 4. 获取属性值
product_ids = [prod['id'] for prod in soup.select('.product')]
print(f"产品ID列表: {product_ids}")

# 5. 从元素中提取数据
products_data = []
for product in soup.select('.product'):
    name = product.select_one('.name').text
    price = product.select_one('.price').text
    # 提取价格数字
    price_value = float(price.replace('¥', '').replace(',', ''))
    rating_text = product.select_one('.rating').text
    rating = float(rating_text.split(':')[1].strip())
    
    products_data.append({
        'id': product['id'],
        'name': name,
        'price': price_value,
        'rating': rating
    })

import pandas as pd
df = pd.DataFrame(products_data)
print(df)
        """, language="python")
    
    # 实际爬虫示例 - 使用本地模拟网页
    st.subheader("爬虫实例演示")
    
    st.markdown("""
    以下是一个使用模拟电商网页的爬虫示例。我们将提取产品名称、价格、评分等信息。
    """)
    
    # 加载模拟HTML文件
    html_content, soup = load_html_file('mock_html/mock_shop.html')
    
    if html_content and soup:
        # 展示部分HTML源码
        with st.expander("查看部分HTML源码"):
            st.code(html_content[:1500] + "...", language="html")
        
        # 展示爬虫代码
        with st.expander("查看爬虫代码"):
            st.code("""
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

# 在实际环境中，这里应该是一个网页URL
# url = "https://example.com/shop"
# response = requests.get(url)
# html_content = response.text
# soup = BeautifulSoup(html_content, 'html.parser')

# 加载本地HTML文件以进行演示
with open('mock_shop.html', 'r', encoding='utf-8') as f:
    html_content = f.read()
soup = BeautifulSoup(html_content, 'html.parser')

# 提取所有产品信息
products = []
product_elements = soup.select('.product')

for product in product_elements:
    product_id = product.get('id', '')
    title = product.select_one('.product-title').text.strip()
    
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

# 转换为DataFrame
df = pd.DataFrame(products)
print(df.head())
            """, language="python")
        
        # 提取数据并展示
        products = extract_product_data(soup)
        if products:
            df_products = pd.DataFrame(products)
            
            st.subheader("提取结果:")
            st.dataframe(df_products)
            
            # 一些简单的可视化
            st.subheader("基本分析")
            
            # 分类统计
            category_counts = df_products['category'].value_counts()
            st.bar_chart(category_counts)
            
            # 价格分布
            st.subheader("价格分布")
            fig, ax = plt.subplots()
            ax.hist(df_products['price'].dropna(), bins=10)
            ax.set_xlabel('价格 (¥)')
            ax.set_ylabel('产品数量')
            st.pyplot(fig)
            
            # 促销情况
            promo_counts = df_products['is_promotion'].value_counts()
            st.subheader("促销产品比例")
            st.write(f"促销产品: {promo_counts.get(True, 0)}个")
            st.write(f"非促销产品: {promo_counts.get(False, 0)}个")
            
            # 评分与价格的关系
            st.subheader("评分与价格的关系")
            fig, ax = plt.subplots()
            ax.scatter(df_products['price'], df_products['rating'])
            ax.set_xlabel('价格 (¥)')
            ax.set_ylabel('评分')
            st.pyplot(fig)
    else:
        st.error("无法加载模拟HTML文件。")
    
    # 爬虫注意事项
    st.subheader("爬虫注意事项")
    
    st.warning("""
    **合法合规**: 在编写爬虫前，请先阅读目标网站的robots.txt文件和使用条款，确保您的爬虫活动是合法的。
    
    **礼貌爬取**: 控制爬取速度，避免对服务器造成过大负担。在请求之间添加适当的延迟。
    
    **模拟正常行为**: 设置合理的User-Agent和其他HTTP头，模拟真实用户的行为。
    
    **错误处理**: 实现健壮的错误处理机制，应对网络问题和非预期的HTML结构变化。
    
    **数据存储**: 妥善处理和存储收集的数据，尊重数据隐私。
    """)
    
    # 扩展资源
    st.subheader("扩展资源")
    
    st.markdown("""
    - [Requests 文档](https://docs.python-requests.org/)
    - [BeautifulSoup 文档](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
    - [Robots.txt 标准](https://www.robotstxt.org/robotstxt.html)
    - [MDN HTTP 文档](https://developer.mozilla.org/zh-CN/docs/Web/HTTP)
    """)

# 避免matplotlib冲突
import matplotlib.pyplot as plt 