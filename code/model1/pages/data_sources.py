import streamlit as st
import pandas as pd
import numpy as np
import sqlite3
import json
import tempfile
import os
from io import StringIO

def show():
    """显示数据源页面内容"""
    st.header("数据源")
    
    st.markdown("""
    ## 数据源概述
    
    在商业智能和数据分析中，数据可以来自多种来源。了解不同类型的数据源及其获取方法是数据采集的第一步。
    """)
    
    st.subheader("常见数据源类型")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 1. Web APIs
        Web API是一种通过HTTP协议访问的编程接口，许多网站和服务提供API以允许程序化访问其数据。
        
        **特点**:
        - 结构化数据（通常为JSON或XML格式）
        - 可以通过程序自动获取
        - 通常需要API密钥或认证
        - 可能有访问限制（如速率限制）
        
        **示例**: Twitter API, GitHub API, 天气数据API
        """)
        
        st.markdown("""
        ### 2. 数据库
        数据库是许多组织存储结构化数据的主要方式。
        
        **类型**:
        - 关系型数据库 (MySQL, PostgreSQL, SQLite)
        - NoSQL数据库 (MongoDB, Cassandra)
        - 时序数据库 (InfluxDB, TimescaleDB)
        
        **特点**:
        - 高度结构化
        - 支持复杂查询
        - 需要连接凭证
        - 可以通过SQL或其他查询语言访问
        """)
    
    with col2:
        st.markdown("""
        ### 3. 结构化文件
        结构化文件以特定格式存储数据，便于程序处理。
        
        **类型**:
        - CSV（逗号分隔值）
        - Excel文件
        - JSON文件
        - XML文件
        - Parquet, Arrow等大数据文件格式
        
        **特点**:
        - 易于共享和传输
        - 可以使用专门的库处理
        - 适合中小规模数据
        """)
        
        st.markdown("""
        ### 4. 非结构化数据
        非结构化数据没有预定义的数据模型，需要额外处理才能提取信息。
        
        **类型**:
        - 网页HTML
        - 文本文档
        - 图像
        - 音频文件
        - 视频文件
        
        **特点**:
        - 数据提取复杂
        - 需要特殊处理技术（如网络爬虫、OCR、语音识别）
        - 信息丰富但需要结构化
        """)
    
    st.markdown("""
    ### 5. 动态Web内容
    许多现代网站使用JavaScript动态加载内容，这类数据需要特殊的抓取技术。
    
    **特点**:
    - 内容在客户端动态生成
    - 普通HTTP请求可能无法获取完整数据
    - 需要使用浏览器自动化工具（如Selenium, Playwright）
    - 可能需要处理AJAX请求
    """)
    
    # 代码示例部分
    st.header("数据获取示例")
    
    tabs = st.tabs(["Web API", "CSV/Excel文件", "数据库", "网页数据"])
    
    # Web API 选项卡
    with tabs[0]:
        st.subheader("从Web API获取数据")
        st.markdown("""
        使用Python的`requests`库从API获取数据是常见的数据采集方法。以下是从一个假设的API获取数据的示例：
        """)
        
        with st.expander("查看代码示例"):
            st.code("""
import requests
import json

# API endpoint URL
url = "https://api.example.com/data"

# 添加请求参数
params = {
    "category": "electronics",
    "limit": 100,
    "sort": "price"
}

# 添加认证头信息（如果需要）
headers = {
    "Authorization": "Bearer YOUR_API_KEY",
    "Content-Type": "application/json"
}

# 发送GET请求
response = requests.get(url, params=params, headers=headers)

# 检查响应状态
if response.status_code == 200:
    # 解析JSON响应
    data = response.json()
    
    # 转换为Pandas DataFrame
    import pandas as pd
    df = pd.DataFrame(data['items'])
    
    # 显示数据
    print(df.head())
else:
    print(f"Error: API返回了状态码 {response.status_code}")
    print(response.text)
            """, language="python")
            
            # 模拟API响应
            mock_api_resp = {
                "status": "success",
                "count": 5,
                "items": [
                    {"id": 1, "name": "笔记本电脑", "price": 5999, "category": "电子产品"},
                    {"id": 2, "name": "智能手机", "price": 3999, "category": "电子产品"},
                    {"id": 3, "name": "无线耳机", "price": 999, "category": "电子产品"},
                    {"id": 4, "name": "智能手表", "price": 1599, "category": "电子产品"},
                    {"id": 5, "name": "平板电脑", "price": 2999, "category": "电子产品"}
                ]
            }
            
            # 展示模拟的API响应
            st.subheader("模拟API响应:")
            st.json(mock_api_resp)
            
            # 展示转换后的DataFrame
            st.subheader("转换为Pandas DataFrame:")
            df_api = pd.DataFrame(mock_api_resp["items"])
            st.dataframe(df_api)
    
    # CSV/Excel文件选项卡
    with tabs[1]:
        st.subheader("读取CSV和Excel文件")
        st.markdown("""
        Pandas库使读取结构化文件变得简单，以下是读取CSV和Excel文件的示例：
        """)
        
        with st.expander("查看CSV读取代码"):
            st.code("""
import pandas as pd

# 读取CSV文件
df_csv = pd.read_csv('data.csv')

# 基本信息
print(df_csv.info())
print(df_csv.describe())

# 显示前几行
print(df_csv.head())
            """, language="python")
            
            # 创建示例CSV数据
            csv_data = """产品ID,产品名称,价格,类别,库存
P001,笔记本电脑,5999,电子产品,25
P002,智能手机,3999,电子产品,50
P003,无线耳机,999,电子产品,100
P004,智能手表,1599,电子产品,30
P005,平板电脑,2999,电子产品,15"""
            
            # 显示CSV数据
            df_csv = pd.read_csv(StringIO(csv_data))
            st.subheader("CSV数据示例:")
            st.dataframe(df_csv)
        
        with st.expander("查看Excel读取代码"):
            st.code("""
import pandas as pd

# 读取Excel文件
df_excel = pd.read_excel('data.xlsx', sheet_name='Sheet1')

# 读取特定列
selected_cols = df_excel[['产品ID', '产品名称', '价格']]

# 条件筛选
expensive_products = df_excel[df_excel['价格'] > 3000]

# 保存为新文件
expensive_products.to_excel('expensive_products.xlsx', index=False)
            """, language="python")
            
            # 显示与CSV相同的数据，但作为Excel数据
            st.subheader("Excel数据示例 (与CSV相同):")
            st.dataframe(df_csv)
    
    # 数据库选项卡
    with tabs[2]:
        st.subheader("查询数据库")
        st.markdown("""
        Python可以通过多种库连接不同类型的数据库。以下是SQLite示例：
        """)
        
        with st.expander("查看SQLite查询代码"):
            st.code("""
import sqlite3
import pandas as pd

# 连接到SQLite数据库
conn = sqlite3.connect('store.db')

# 创建游标对象
cursor = conn.cursor()

# 执行SQL查询
query = '''
SELECT 
    products.product_id, 
    products.name, 
    products.price, 
    categories.category_name,
    inventory.stock_quantity
FROM 
    products
JOIN 
    categories ON products.category_id = categories.category_id
JOIN 
    inventory ON products.product_id = inventory.product_id
WHERE 
    products.price > 1000
ORDER BY 
    products.price DESC
'''

# 使用pandas直接读取查询结果
df = pd.read_sql_query(query, conn)

# 显示结果
print(df.head())

# 关闭连接
conn.close()
            """, language="python")
            
            # 创建临时SQLite数据库
            with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as temp_db:
                db_path = temp_db.name
            
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # 创建表格
            cursor.execute('''
            CREATE TABLE categories (
                category_id INTEGER PRIMARY KEY,
                category_name TEXT NOT NULL
            )
            ''')
            
            cursor.execute('''
            CREATE TABLE products (
                product_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                price REAL NOT NULL,
                category_id INTEGER,
                FOREIGN KEY (category_id) REFERENCES categories (category_id)
            )
            ''')
            
            cursor.execute('''
            CREATE TABLE inventory (
                inventory_id INTEGER PRIMARY KEY,
                product_id TEXT,
                stock_quantity INTEGER NOT NULL,
                FOREIGN KEY (product_id) REFERENCES products (product_id)
            )
            ''')
            
            # 插入示例数据
            cursor.execute("INSERT INTO categories VALUES (1, '电子产品')")
            cursor.execute("INSERT INTO categories VALUES (2, '服装')")
            
            products = [
                ("P001", "笔记本电脑", 5999, 1),
                ("P002", "智能手机", 3999, 1),
                ("P003", "无线耳机", 999, 1),
                ("P004", "智能手表", 1599, 1),
                ("P005", "平板电脑", 2999, 1)
            ]
            
            cursor.executemany("INSERT INTO products VALUES (?, ?, ?, ?)", products)
            
            inventory = [
                (1, "P001", 25),
                (2, "P002", 50),
                (3, "P003", 100),
                (4, "P004", 30),
                (5, "P005", 15)
            ]
            
            cursor.executemany("INSERT INTO inventory VALUES (?, ?, ?)", inventory)
            
            conn.commit()
            
            # 执行查询并显示结果
            query = '''
            SELECT 
                products.product_id, 
                products.name, 
                products.price, 
                categories.category_name,
                inventory.stock_quantity
            FROM 
                products
            JOIN 
                categories ON products.category_id = categories.category_id
            JOIN 
                inventory ON products.product_id = inventory.product_id
            ORDER BY 
                products.price DESC
            '''
            
            df_sql = pd.read_sql_query(query, conn)
            conn.close()
            os.unlink(db_path)  # 删除临时数据库文件
            
            st.subheader("SQLite查询结果:")
            st.dataframe(df_sql)
    
    # 网页数据选项卡
    with tabs[3]:
        st.subheader("从网页获取数据")
        st.markdown("""
        使用BeautifulSoup从HTML页面提取数据是网络爬虫的基础技术。以下是一个简单示例：
        """)
        
        with st.expander("查看HTML解析代码"):
            st.code("""
import requests
from bs4 import BeautifulSoup
import pandas as pd

# 发送请求获取网页内容
url = "https://example.com/products"
response = requests.get(url)
html_content = response.text

# 使用BeautifulSoup解析HTML
soup = BeautifulSoup(html_content, 'html.parser')

# 查找所有产品项
products = []
product_elements = soup.select('.product-item')

for product in product_elements:
    # 提取产品信息
    name = product.select_one('.product-name').text.strip()
    price_text = product.select_one('.product-price').text.strip()
    price = float(price_text.replace('¥', '').replace(',', ''))
    
    # 提取评分（如果有）
    rating_elem = product.select_one('.product-rating')
    rating = float(rating_elem.text) if rating_elem else None
    
    products.append({
        'name': name,
        'price': price,
        'rating': rating
    })

# 转换为DataFrame
df = pd.DataFrame(products)
print(df.head())
            """, language="python")
            
            # 模拟HTML内容
            html_example = """
<div class="product-list">
    <div class="product-item">
        <h3 class="product-name">笔记本电脑 - 超薄商务本</h3>
        <div class="product-price">¥5,999</div>
        <div class="product-rating">4.7</div>
    </div>
    <div class="product-item">
        <h3 class="product-name">智能手机 - 旗舰机型</h3>
        <div class="product-price">¥3,999</div>
        <div class="product-rating">4.5</div>
    </div>
    <div class="product-item">
        <h3 class="product-name">无线耳机 - 降噪版</h3>
        <div class="product-price">¥999</div>
        <div class="product-rating">4.3</div>
    </div>
</div>
            """
            
            st.subheader("HTML示例:")
            st.code(html_example, language="html")
            
            # 解析示例HTML
            soup = BeautifulSoup(html_example, 'html.parser')
            products = []
            
            for product in soup.select('.product-item'):
                name = product.select_one('.product-name').text.strip()
                price_text = product.select_one('.product-price').text.strip()
                price = float(price_text.replace('¥', '').replace(',', ''))
                rating = float(product.select_one('.product-rating').text)
                
                products.append({
                    'name': name,
                    'price': price,
                    'rating': rating
                })
            
            df_html = pd.DataFrame(products)
            
            st.subheader("解析结果:")
            st.dataframe(df_html) 