"""基础网络爬虫模块，介绍爬虫基本概念和技术"""

import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup

# 导入文本展示组件
from ...components.text_displays import (
    show_code_block, show_info_card, show_steps, 
    show_tutorial, show_warning_box
)


def show_http_basics():
    """展示HTTP基础知识"""
    st.subheader("HTTP基础知识")
    
    st.markdown("""
    HTTP (HyperText Transfer Protocol) 是网络通信的基础，了解它对网络爬虫至关重要。
    """)
    
    # HTTP请求方法
    show_info_card(
        "HTTP请求方法", 
        """
        * **GET**: 请求资源，参数附加在URL中
        * **POST**: 提交数据，参数在请求体中
        * **HEAD**: 类似GET但只请求头部
        * **PUT**: 上传或替换资源
        * **DELETE**: 删除资源
        
        网络爬虫最常用的是**GET**和**POST**方法。
        """,
        icon="🔄"
    )
    
    # HTTP状态码
    col1, col2 = st.columns(2)
    
    with col1:
        show_info_card(
            "常见HTTP状态码", 
            """
            * **200 OK**: 请求成功
            * **301/302**: 重定向
            * **400**: 错误请求
            * **403**: 禁止访问
            * **404**: 资源不存在
            * **500**: 服务器错误
            """,
            icon="🔢"
        )
    
    with col2:
        show_info_card(
            "HTTP头部信息", 
            """
            * **User-Agent**: 客户端标识
            * **Cookie**: 会话信息
            * **Referer**: 来源页面
            * **Content-Type**: 内容类型
            * **Accept**: 可接受的响应类型
            """,
            icon="📋"
        )


def show_requests_tutorial():
    """展示Requests库教程"""
    st.subheader("使用Requests发送请求")
    
    st.markdown("""
    [Requests](https://requests.readthedocs.io/)是Python中最流行的HTTP库，它让HTTP请求变得简单和人性化。
    """)
    
    # 安装Requests
    show_code_block(
        "pip install requests",
        language="bash",
        title="安装Requests"
    )
    
    # 基本用法
    show_tutorial(
        "Requests基本用法",
        [
            {
                "title": "发送GET请求",
                "content": "最简单的GET请求示例：",
                "code": """
import requests

# 发送GET请求
response = requests.get('https://httpbin.org/get')

# 查看响应状态码
print(response.status_code)  # 应该是200

# 查看响应内容
print(response.text)  # 返回文本内容
print(response.json())  # 解析JSON响应"""
            },
            {
                "title": "设置请求参数",
                "content": "使用params参数发送查询字符串：",
                "code": """
# 带参数的GET请求
params = {'key1': 'value1', 'key2': 'value2'}
response = requests.get('https://httpbin.org/get', params=params)

# URL将变成https://httpbin.org/get?key1=value1&key2=value2
print(response.url)"""
            },
            {
                "title": "设置请求头",
                "content": "添加自定义头部信息，比如模拟浏览器访问：",
                "code": """
# 设置请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}
response = requests.get('https://httpbin.org/get', headers=headers)"""
            },
            {
                "title": "发送POST请求",
                "content": "发送POST请求通常用于提交表单数据：",
                "code": """
# 发送POST请求
data = {'username': 'demo', 'password': 'password'}
response = requests.post('https://httpbin.org/post', data=data)

# 查看响应
print(response.json())"""
            },
            {
                "title": "处理响应",
                "content": "Requests提供了多种处理响应的方法：",
                "code": """
response = requests.get('https://api.github.com/events')

# 检查请求是否成功
if response.status_code == 200:
    # 获取响应内容的不同形式
    text_content = response.text  # 文本形式
    json_content = response.json()  # JSON形式（如果响应是JSON）
    binary_content = response.content  # 二进制形式

# 获取响应头信息
headers = response.headers
content_type = headers['Content-Type']

# 响应编码
print(response.encoding)  # 返回猜测的编码
response.encoding = 'utf-8'  # 设置编码"""
            }
        ]
    )
    
    # 请求超时和异常处理
    show_code_block(
        """
import requests
from requests.exceptions import RequestException

try:
    # 设置5秒超时
    response = requests.get('https://httpbin.org/delay/10', timeout=5)
    response.raise_for_status()  # 如果状态码不是200，抛出异常
except requests.Timeout:
    print("请求超时")
except requests.HTTPError as e:
    print(f"HTTP错误: {e}")
except RequestException as e:
    print(f"请求异常: {e}")
""",
        title="请求超时和异常处理"
    )
    
    # 实用技巧
    show_warning_box(
        """
        爬虫最佳实践：
        1. 总是添加超时设置，避免程序无限等待
        2. 始终进行异常处理
        3. 尊重服务器，控制请求频率（考虑使用time.sleep()）
        4. 使用User-Agent模拟真实浏览器，避免被拒绝访问
        """,
        title="爬虫实用技巧"
    )


def show_beautifulsoup_tutorial():
    """展示BeautifulSoup教程"""
    st.subheader("使用BeautifulSoup解析HTML")
    
    st.markdown("""
    [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)是一个用于从HTML和XML文件中提取数据的Python库。
    它提供了简单的方法来导航、搜索和修改解析树，非常适合网页数据提取。
    """)
    
    # 安装BeautifulSoup
    show_code_block(
        "pip install beautifulsoup4 lxml",
        language="bash",
        title="安装BeautifulSoup和解析器"
    )
    
    # 基本用法
    show_tutorial(
        "BeautifulSoup基本用法",
        [
            {
                "title": "创建BeautifulSoup对象",
                "content": "首先需要将HTML文档解析为BeautifulSoup对象：",
                "code": """
from bs4 import BeautifulSoup

# HTML字符串
html_doc = '''
<html>
    <head><title>网页标题</title></head>
    <body>
        <h1 id="main-title">Hello World</h1>
        <p class="content">这是一个段落。</p>
        <p class="content">这是另一个段落。</p>
        <ul>
            <li><a href="https://example.com/page1">链接1</a></li>
            <li><a href="https://example.com/page2">链接2</a></li>
        </ul>
    </body>
</html>
'''

# 创建BeautifulSoup对象
soup = BeautifulSoup(html_doc, 'lxml')  # 使用lxml解析器

# 格式化输出HTML
print(soup.prettify())"""
            },
            {
                "title": "简单导航和搜索",
                "content": "BeautifulSoup提供了多种方法来导航和搜索解析树：",
                "code": """
# 查找第一个标签
title_tag = soup.title
print(title_tag)  # <title>网页标题</title>
print(title_tag.string)  # 网页标题

# 查找所有标签
all_paragraphs = soup.find_all('p')
for p in all_paragraphs:
    print(p.text)

# 通过属性查找
main_title = soup.find(id='main-title')
print(main_title.text)  # Hello World

# 通过CSS选择器查找
content_paragraphs = soup.select('.content')
for p in content_paragraphs:
    print(p.text)"""
            },
            {
                "title": "CSS选择器",
                "content": "BeautifulSoup支持多种CSS选择器语法：",
                "code": """
# 通过标签名查找
all_links = soup.select('a')

# 通过类名查找
content_elements = soup.select('.content')

# 通过ID查找
main_title = soup.select('#main-title')

# 组合查找
list_links = soup.select('ul li a')

# 查找属性
links = soup.select('a[href^="https"]')  # 以https开头的链接"""
            },
            {
                "title": "提取数据",
                "content": "从标签中提取数据：",
                "code": """
# 提取文本内容
for paragraph in soup.find_all('p'):
    print(paragraph.text)  # 获取文本内容

# 提取属性值
for link in soup.find_all('a'):
    print(link.get('href'))  # 获取href属性
    # 或者使用 link['href']"""
            }
        ]
    )
    
    # 实际示例
    show_code_block(
        """
import requests
from bs4 import BeautifulSoup

# 获取网页内容
url = 'https://news.ycombinator.com/'
response = requests.get(url)
html_content = response.text

# 解析HTML
soup = BeautifulSoup(html_content, 'lxml')

# 提取新闻标题和链接
news_items = []
for item in soup.select('.titleline > a'):
    title = item.text
    link = item.get('href')
    news_items.append({'title': title, 'link': link})

# 显示结果
for item in news_items[:5]:  # 只显示前5条
    print(f"标题: {item['title']}")
    print(f"链接: {item['link']}")
    print('-' * 50)
""",
        title="实际爬虫示例：爬取Hacker News头条"
    )
    
    # 提示和技巧
    show_info_card(
        "BeautifulSoup技巧", 
        """
        * 使用**.find()**找第一个匹配元素，使用**.find_all()**找所有匹配元素
        * **.select()**方法支持CSS选择器，功能强大且直观
        * 结合**正则表达式**可以实现更复杂的匹配
        * 对于处理大型文档，考虑使用**lxml**解析器提高性能
        * **NavigableString**对象表示标签内的文本内容
        * 使用**.decompose()**方法可以移除不需要的元素，如广告
        """,
        icon="💡"
    )


def show_data_extraction():
    """展示数据提取技术"""
    st.subheader("提取网页数据")
    
    st.markdown("""
    网页数据提取是爬虫的核心任务。借助Requests和BeautifulSoup的组合，我们可以高效地从网页中提取所需信息。
    """)
    
    # 常见数据提取模式
    show_steps(
        [
            {
                "title": "识别目标数据",
                "content": """
                在开始爬取之前，先明确需要获取的数据类型：
                * 文本内容（标题、段落、描述等）
                * 链接URL
                * 图片URL
                * 表格数据
                * 列表数据
                
                使用浏览器开发者工具（F12）检查目标元素的HTML结构，找出唯一标识它们的特征（ID、类名、属性等）。
                """
            },
            {
                "title": "获取网页内容",
                "content": "使用Requests库获取网页HTML内容",
                "code": """
import requests

url = "https://example.com"
response = requests.get(url)
html_content = response.text"""
            },
            {
                "title": "解析页面结构",
                "content": "使用BeautifulSoup解析HTML，创建可查询的解析树",
                "code": """
from bs4 import BeautifulSoup

soup = BeautifulSoup(html_content, 'lxml')"""
            },
            {
                "title": "定位和提取数据",
                "content": "使用BeautifulSoup的查询方法定位并提取目标数据",
                "code": """
# 提取所有标题
titles = []
for heading in soup.find_all(['h1', 'h2', 'h3']):
    titles.append(heading.text.strip())

# 提取所有链接
links = []
for a_tag in soup.find_all('a'):
    link = a_tag.get('href')
    if link and not link.startswith('#'):  # 过滤页内锚点
        links.append(link)
        
# 提取表格数据
tables_data = []
for table in soup.find_all('table'):
    table_data = []
    for row in table.find_all('tr'):
        row_data = [cell.text.strip() for cell in row.find_all(['td', 'th'])]
        if row_data:  # 确保行不为空
            table_data.append(row_data)
    tables_data.append(table_data)"""
            },
            {
                "title": "数据清理与结构化",
                "content": "清理提取的数据并组织成结构化格式",
                "code": """
import pandas as pd

# 清理文本数据
def clean_text(text):
    # 移除多余空白
    text = ' '.join(text.split())
    # 其他清理操作...
    return text

# 将提取的数据转换为DataFrame
if tables_data:
    # 假设第一个表格的第一行是表头
    headers = tables_data[0][0]
    data = tables_data[0][1:]
    df = pd.DataFrame(data, columns=headers)
    
    # 数据清洗
    df = df.applymap(clean_text)
    
    print(df.head())"""
            },
            {
                "title": "存储数据",
                "content": "将提取的数据保存为需要的格式",
                "code": """
# 保存为CSV
df.to_csv('extracted_data.csv', index=False)

# 保存为JSON
df.to_json('extracted_data.json', orient='records')

# 保存为Excel
df.to_excel('extracted_data.xlsx', index=False)"""
            }
        ],
        title="数据提取步骤"
    )
    
    # 提取不同类型的数据示例
    example_tabs = st.tabs(["提取文本", "提取链接", "提取表格", "提取图片"])
    
    with example_tabs[0]:
        show_code_block(
            """
# 提取文章正文
article_content = soup.find('article', class_='post-content')
if article_content:
    # 提取所有段落文本
    paragraphs = [p.text.strip() for p in article_content.find_all('p')]
    
    # 合并段落
    full_text = '\\n\\n'.join(paragraphs)
    
    # 移除多余空白
    import re
    full_text = re.sub(r'\\s+', ' ', full_text)
            """,
            title="提取文章正文"
        )
    
    with example_tabs[1]:
        show_code_block(
            """
# 提取所有链接并规范化URL
from urllib.parse import urljoin

base_url = "https://example.com"
links = []

for a_tag in soup.find_all('a', href=True):
    href = a_tag.get('href')
    
    # 将相对URL转为绝对URL
    absolute_url = urljoin(base_url, href)
    
    # 提取链接文本
    link_text = a_tag.text.strip()
    
    links.append({
        'text': link_text,
        'url': absolute_url
    })
            """,
            title="提取和规范化链接"
        )
    
    with example_tabs[2]:
        show_code_block(
            """
# 提取表格数据到Pandas DataFrame
import pandas as pd

# 定位表格
table = soup.find('table', id='data-table')  # 或者使用class_='table-class'
if table:
    # 提取表头
    headers = []
    header_row = table.find('thead').find('tr')
    for th in header_row.find_all('th'):
        headers.append(th.text.strip())
    
    # 提取表格数据
    rows = []
    for tr in table.find('tbody').find_all('tr'):
        row = []
        for td in tr.find_all('td'):
            row.append(td.text.strip())
        rows.append(row)
    
    # 创建DataFrame
    df = pd.DataFrame(rows, columns=headers)
    print(df.head())
            """,
            title="提取表格数据到DataFrame"
        )
    
    with example_tabs[3]:
        show_code_block(
            """
# 提取所有图片URL
import os
from urllib.parse import urljoin

base_url = "https://example.com"
image_info = []

for img in soup.find_all('img', src=True):
    # 获取图片URL
    img_url = img.get('src')
    absolute_img_url = urljoin(base_url, img_url)
    
    # 获取alt文本
    alt_text = img.get('alt', '')
    
    # 获取图片文件名
    file_name = os.path.basename(img_url)
    
    image_info.append({
        'url': absolute_img_url,
        'alt': alt_text,
        'file_name': file_name
    })

# 下载图片
def download_image(img_url, save_path):
    response = requests.get(img_url, stream=True)
    if response.status_code == 200:
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
        return True
    return False

# 下载前5张图片示例
for i, img in enumerate(image_info[:5]):
    save_path = f"image_{i}_{img['file_name']}"
    success = download_image(img['url'], save_path)
    print(f"下载 {img['url']} 到 {save_path}: {'成功' if success else '失败'}")
            """,
            title="提取和下载图片"
        )
    
    # 提供一个综合案例
    st.markdown("### 综合案例：提取网站产品信息")
    
    show_code_block(
        """
import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin
import time
import random

def scrape_product_info(url):
    # 添加请求头模拟浏览器
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5'
    }
    
    try:
        # 发送请求
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # 检查响应状态
        
        # 解析HTML
        soup = BeautifulSoup(response.text, 'lxml')
        
        # 产品列表容器 (假设产品在具有特定类的div中)
        products = soup.find_all('div', class_='product-item')
        
        all_products = []
        
        for product in products:
            # 提取产品信息
            title_element = product.find('h2', class_='product-title')
            price_element = product.find('span', class_='price')
            rating_element = product.find('div', class_='rating')
            image_element = product.find('img', class_='product-image')
            link_element = product.find('a', class_='product-link')
            
            # 提取数据，提供默认值防止None错误
            title = title_element.text.strip() if title_element else 'No Title'
            price = price_element.text.strip() if price_element else 'No Price'
            rating = rating_element.get('data-rating', 'No Rating') if rating_element else 'No Rating'
            image_url = image_element.get('src') if image_element else None
            product_url = link_element.get('href') if link_element else None
            
            # 规范化URL
            if image_url:
                image_url = urljoin(url, image_url)
            if product_url:
                product_url = urljoin(url, product_url)
            
            # 整合数据
            product_info = {
                'title': title,
                'price': price,
                'rating': rating,
                'image_url': image_url,
                'product_url': product_url
            }
            
            all_products.append(product_info)
            
            # 友好爬取，随机延迟
            time.sleep(random.uniform(0.5, 2.0))
        
        # 转换为DataFrame
        products_df = pd.DataFrame(all_products)
        
        return products_df
    
    except Exception as e:
        print(f"爬取出错: {e}")
        return None

# 使用示例
if __name__ == "__main__":
    target_url = "https://example.com/products"
    df = scrape_product_info(target_url)
    
    if df is not None:
        print(f"成功爬取 {len(df)} 个产品信息")
        df.to_csv('product_data.csv', index=False)
        print("数据已保存到 product_data.csv")
        """,
        title="综合数据提取案例"
    )


def show_simple_example():
    """展示简单爬虫实例"""
    st.subheader("简单爬虫实例")
    
    st.markdown("""
    以下是一个简单但完整的爬虫示例，它爬取一个网页的标题和所有链接：
    """)
    
    # 代码示例
    show_code_block(
        """
import requests
from bs4 import BeautifulSoup
import pandas as pd
import logging
import time

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("scraper.log"),
        logging.StreamHandler()
    ]
)

def scrape_website(url, max_retries=3):
    """
    爬取指定URL的网页标题和链接
    
    参数:
        url (str): 要爬取的网页URL
        max_retries (int): 最大重试次数
    
    返回:
        dict: 包含标题和链接列表的字典
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    retry_count = 0
    while retry_count < max_retries:
        try:
            logging.info(f"正在请求URL: {url}")
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            # 获取网页标题和链接
            soup = BeautifulSoup(response.text, 'lxml')
            title = soup.title.text if soup.title else "无标题"
            
            links = []
            for link in soup.find_all('a', href=True):
                href = link.get('href')
                text = link.text.strip()
                if href and not href.startswith('#'):
                    links.append({
                        'url': href,
                        'text': text if text else "无文本"
                    })
            
            logging.info(f"成功抓取 {url}, 获取到 {len(links)} 个链接")
            
            return {
                'title': title,
                'links': links
            }
            
        except requests.exceptions.RequestException as e:
            retry_count += 1
            wait_time = 2 ** retry_count  # 指数退避
            logging.error(f"请求失败 ({retry_count}/{max_retries}): {e}")
            logging.info(f"等待 {wait_time} 秒后重试...")
            time.sleep(wait_time)
    
    logging.error(f"达到最大重试次数，放弃请求: {url}")
    return None

def save_data(data, output_file='scrape_results.csv'):
    """保存爬取的链接数据到CSV文件"""
    if not data or 'links' not in data:
        logging.error("无数据可保存")
        return False
    
    try:
        df = pd.DataFrame(data['links'])
        df.to_csv(output_file, index=False)
        logging.info(f"数据已保存到 {output_file}")
        return True
    except Exception as e:
        logging.error(f"保存数据失败: {e}")
        return False

def main():
    """主函数"""
    url = "https://example.com"  # 替换为你要爬取的URL
    
    # 爬取数据
    data = scrape_website(url)
    
    if data:
        # 打印网页标题
        print(f"网页标题: {data['title']}")
        
        # 保存链接到CSV
        save_data(data)
        
        # 打印前5个链接
        print("\n前5个链接:")
        for i, link in enumerate(data['links'][:5], 1):
            print(f"{i}. {link['text']} - {link['url']}")
    else:
        print("爬取失败")

if __name__ == "__main__":
    main()
        """,
        title="完整爬虫示例"
    )
    
    # 爬虫项目结构
    st.markdown("### 爬虫项目结构")
    
    project_structure = """
scraper/
├── main.py           # 主入口文件
├── scraper.py        # 爬虫核心功能
├── utils/
│   ├── __init__.py
│   ├── parser.py     # HTML解析功能
│   ├── downloader.py # 下载器
│   └── logger.py     # 日志配置
├── config.py         # 配置参数
├── requirements.txt  # 依赖项
└── data/             # 爬取数据保存目录
    └── .gitkeep
"""
    
    st.code(project_structure)
    
    # 实用技巧
    show_info_card(
        "爬虫实用技巧", 
        """
        1. **增量式爬取**：只爬取新内容，减少服务器负担
        2. **使用代理IP**：避免IP被封
        3. **随机延迟**：模拟人类行为，减少被检测风险
        4. **编写测试**：确保爬虫在网站结构变化时能够快速适应
        5. **定期维护**：网站结构可能随时变化，需要经常更新爬虫
        6. **保存原始数据**：保存原始HTML有助于日后重新解析
        """,
        icon="🚀"
    )


def show_basics():
    """展示基础网络爬虫教程"""
    st.title("网络爬虫基础")
    
    # 介绍
    st.markdown("""
    网络爬虫（Web Crawler或Web Spider）是一种自动化程序，用于系统地浏览万维网并收集数据。
    在本教程中，我们将学习基础的网络爬虫技术，包括HTTP基础知识、使用Requests发送请求、
    使用BeautifulSoup解析HTML，以及如何提取和存储数据。
    """)
    
    # 目录
    toc = st.selectbox(
        "选择学习内容",
        ["HTTP基础知识", "使用Requests发送请求", "使用BeautifulSoup解析HTML", "提取网页数据", "简单爬虫实例"]
    )
    
    st.markdown("---")
    
    # 根据选择显示相应内容
    if toc == "HTTP基础知识":
        show_http_basics()
    elif toc == "使用Requests发送请求":
        show_requests_tutorial()
    elif toc == "使用BeautifulSoup解析HTML":
        show_beautifulsoup_tutorial()
    elif toc == "提取网页数据":
        show_data_extraction()
    elif toc == "简单爬虫实例":
        show_simple_example()
    
    # 互动组件 - 简单爬虫测试
    st.markdown("---")
    st.subheader("互动测试：链接提取器")
    
    with st.expander("尝试一下链接提取器"):
        test_url = st.text_input("输入一个网址", "https://www.example.com")
        
        if st.button("提取链接"):
            try:
                with st.spinner("正在获取数据..."):
                    # 发送请求
                    response = requests.get(test_url, timeout=10)
                    
                    # 解析HTML
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # 提取所有链接
                    links = []
                    for a_tag in soup.find_all('a', href=True):
                        href = a_tag.get('href')
                        text = a_tag.text.strip()
                        links.append({"text": text if text else "无文本", "url": href})
                    
                    # 显示结果
                    if links:
                        st.success(f"成功提取 {len(links)} 个链接")
                        df = pd.DataFrame(links)
                        st.dataframe(df)
                    else:
                        st.info("没有找到链接")
                        
            except Exception as e:
                st.error(f"发生错误: {str(e)}")


if __name__ == "__main__":
    show_basics() 