import streamlit as st
import pandas as pd
import os
import sys

# 添加项目根目录到Python路径，以便导入utils模块
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.helpers import generate_example_data

def show():
    """显示高级爬虫技术页面内容"""
    st.header("高级爬虫技术")
    
    st.markdown("""
    ## Scrapy框架介绍
    
    Scrapy是一个功能强大的爬虫框架，专为大规模网页抓取而设计。它提供了一套完整的工具链，包括请求、响应处理、内容提取和数据存储等功能。
    
    ### Scrapy的核心组件
    
    - **Spider**：定义如何抓取网站和解析内容
    - **Selector**：使用XPath或CSS选择器从网页提取数据
    - **Item**：定义要抓取的数据结构
    - **Item Pipeline**：处理Spider提取的数据，如清洗、验证和存储
    - **Downloader**：负责获取网页的组件
    - **Scheduler**：管理请求队列
    - **Middleware**：在Scrapy请求/响应处理过程中插入自定义功能
    """)
    
    # Scrapy项目结构
    st.subheader("Scrapy项目结构")
    
    st.code("""
myproject/
├── scrapy.cfg            # 项目配置文件
└── myproject/            # 项目模块，导入代码时使用
    ├── __init__.py
    ├── items.py          # 项目items定义
    ├── middlewares.py    # 项目middlewares
    ├── pipelines.py      # 项目pipelines
    ├── settings.py       # 项目设置
    └── spiders/          # 放置spider的目录
        ├── __init__.py
        └── myspider.py   # 爬虫实现
    """, language="text")
    
    # 基本Scrapy爬虫示例
    st.subheader("基本Scrapy爬虫示例")
    
    with st.expander("查看Spider代码"):
        st.code("""
# myproject/spiders/product_spider.py
import scrapy
from myproject.items import ProductItem

class ProductSpider(scrapy.Spider):
    name = 'products'  # 爬虫的唯一名称
    allowed_domains = ['example.com']  # 限制爬取的域名
    start_urls = ['https://example.com/products']  # 开始URL列表
    
    def parse(self, response):
        """解析产品列表页"""
        # 使用CSS选择器提取产品链接
        product_links = response.css('div.product-item a::attr(href)').getall()
        
        # 处理每个产品链接
        for link in product_links:
            # 构建绝对URL并发送请求
            yield response.follow(link, self.parse_product)
            
        # 处理分页
        next_page = response.css('a.next-page::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)
    
    def parse_product(self, response):
        """解析产品详情页"""
        product = ProductItem()
        
        product['name'] = response.css('h1.product-title::text').get()
        product['price'] = response.css('span.price::text').get()
        product['description'] = response.css('div.description::text').get()
        product['category'] = response.css('ul.breadcrumb li:nth-child(2)::text').get()
        product['sku'] = response.css('span.sku::text').get()
        product['availability'] = response.css('span.availability::text').get()
        product['image_urls'] = response.css('div.product-images img::attr(src)').getall()
        
        yield product
        """, language="python")
    
    with st.expander("查看Items代码"):
        st.code("""
# myproject/items.py
import scrapy

class ProductItem(scrapy.Item):
    name = scrapy.Field()
    price = scrapy.Field()
    description = scrapy.Field()
    category = scrapy.Field()
    sku = scrapy.Field()
    availability = scrapy.Field()
    image_urls = scrapy.Field()
        """, language="python")
    
    with st.expander("查看Pipelines代码"):
        st.code("""
# myproject/pipelines.py
import re
import sqlite3

class PricePipeline:
    """处理价格数据的Pipeline"""
    
    def process_item(self, item, spider):
        # 提取价格中的数字
        if 'price' in item:
            price_text = item['price']
            if price_text:
                # 去除货币符号和逗号，提取数字
                price_value = re.sub(r'[^\d.]', '', price_text)
                try:
                    item['price'] = float(price_value)
                except ValueError:
                    spider.logger.warning(f"无法转换价格: {price_text}")
        return item

class SQLitePipeline:
    """将数据存储到SQLite数据库的Pipeline"""
    
    def __init__(self, db_path):
        self.db_path = db_path
    
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            db_path=crawler.settings.get('SQLITE_DB_PATH', 'products.db')
        )
    
    def open_spider(self, spider):
        self.conn = sqlite3.connect(self.db_path)
        self.cur = self.conn.cursor()
        # 创建表
        self.cur.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            price REAL,
            category TEXT,
            sku TEXT UNIQUE,
            description TEXT,
            availability TEXT
        )
        ''')
    
    def close_spider(self, spider):
        self.conn.close()
    
    def process_item(self, item, spider):
        self.cur.execute('''
        INSERT OR REPLACE INTO products (name, price, category, sku, description, availability)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            item.get('name'),
            item.get('price'),
            item.get('category'),
            item.get('sku'),
            item.get('description'),
            item.get('availability')
        ))
        self.conn.commit()
        return item
        """, language="python")
    
    with st.expander("查看Settings配置"):
        st.code("""
# myproject/settings.py
BOT_NAME = 'myproject'

SPIDER_MODULES = ['myproject.spiders']
NEWSPIDER_MODULE = 'myproject.spiders'

# 遵守robots.txt规则
ROBOTSTXT_OBEY = True

# 配置最大并发请求数
CONCURRENT_REQUESTS = 16

# 下载延迟
DOWNLOAD_DELAY = 1

# 启用Cookie
COOKIES_ENABLED = True

# 配置默认的请求头
DEFAULT_REQUEST_HEADERS = {
   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
   'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
}

# 启用的Pipeline
ITEM_PIPELINES = {
   'myproject.pipelines.PricePipeline': 300,
   'myproject.pipelines.SQLitePipeline': 800,
}

# SQLite数据库路径
SQLITE_DB_PATH = 'products.db'

# 配置日志级别
LOG_LEVEL = 'INFO'
        """, language="python")
    
    # 运行Scrapy
    st.subheader("运行Scrapy爬虫")
    
    st.markdown("""
    Scrapy爬虫可以通过命令行运行，也可以通过程序代码运行：
    """)
    
    with st.expander("查看命令行运行方式"):
        st.code("""
# 创建项目
scrapy startproject myproject

# 进入项目目录
cd myproject

# 生成爬虫
scrapy genspider products example.com

# 运行爬虫
scrapy crawl products

# 将爬取结果保存为JSON
scrapy crawl products -o products.json

# 查看爬虫列表
scrapy list

# 使用scrapy shell测试
scrapy shell "https://example.com/products"
        """, language="bash")
    
    with st.expander("查看代码运行方式"):
        st.code("""
# run_spider.py
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from myproject.spiders.product_spider import ProductSpider

def run_spider():
    # 获取settings.py中的设置
    settings = get_project_settings()
    
    # 可以在这里覆盖设置
    settings.set('LOG_LEVEL', 'INFO')
    settings.set('FEED_FORMAT', 'json')
    settings.set('FEED_URI', 'products.json')
    
    # 创建爬虫进程
    process = CrawlerProcess(settings)
    
    # 添加爬虫
    process.crawl(ProductSpider)
    
    # 启动爬虫进程
    process.start()  # 这个方法会阻塞，直到爬虫完成

if __name__ == '__main__':
    run_spider()
        """, language="python")
    
    # Scrapy高级功能
    st.header("Scrapy高级功能")
    
    # 中间件示例
    st.subheader("下载中间件示例")
    
    with st.expander("查看随机User-Agent中间件"):
        st.code("""
# middlewares.py
import random
from scrapy import signals

class RandomUserAgentMiddleware:
    """随机切换User-Agent的中间件"""
    
    def __init__(self, user_agents):
        self.user_agents = user_agents
    
    @classmethod
    def from_crawler(cls, crawler):
        # 从settings中获取USER_AGENTS列表
        user_agents = crawler.settings.getlist('USER_AGENTS')
        if not user_agents:
            user_agents = [
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1'
            ]
        
        # 实例化中间件
        middleware = cls(user_agents)
        
        # 将中间件实例连接到spider_opened信号
        crawler.signals.connect(middleware.spider_opened, signal=signals.spider_opened)
        
        return middleware
    
    def spider_opened(self, spider):
        spider.logger.info('RandomUserAgentMiddleware已启用')
    
    def process_request(self, request, spider):
        # 为每个请求随机选择一个User-Agent
        user_agent = random.choice(self.user_agents)
        request.headers['User-Agent'] = user_agent
        spider.logger.debug(f'使用User-Agent: {user_agent}')
        """, language="python")
    
    # 在settings.py中启用中间件
    with st.expander("在settings.py中配置中间件"):
        st.code("""
# settings.py
# 启用下载中间件
DOWNLOADER_MIDDLEWARES = {
    'myproject.middlewares.RandomUserAgentMiddleware': 400,
}

# User-Agent列表
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1'
]
        """, language="python")
    
    # 处理分页和翻页
    st.subheader("处理分页和AJAX加载内容")
    
    with st.expander("查看处理分页的Spider"):
        st.code("""
import scrapy
import json

class AjaxProductSpider(scrapy.Spider):
    name = 'ajax_products'
    allowed_domains = ['example.com']
    start_urls = ['https://example.com/api/products?page=1']
    
    def parse(self, response):
        """解析API返回的JSON数据"""
        # 解析JSON响应
        data = json.loads(response.text)
        
        # 提取产品数据
        for product in data['products']:
            yield {
                'id': product['id'],
                'name': product['name'],
                'price': product['price'],
                'category': product['category'],
                'description': product['description']
            }
        
        # 处理分页
        current_page = data['page']
        total_pages = data['total_pages']
        
        if current_page < total_pages:
            next_page = current_page + 1
            next_url = f'https://example.com/api/products?page={next_page}'
            yield scrapy.Request(next_url, callback=self.parse)
        """, language="python")
    
    # 处理表单和登录
    st.subheader("处理表单和登录")
    
    with st.expander("查看处理登录的Spider"):
        st.code("""
import scrapy
from scrapy.http import FormRequest

class LoginSpider(scrapy.Spider):
    name = 'login_example'
    allowed_domains = ['example.com']
    start_urls = ['https://example.com/login']
    
    def parse(self, response):
        """处理登录页面"""
        # 提取CSRF令牌（很多网站会使用）
        csrf_token = response.css('input[name="csrf_token"]::attr(value)').get()
        
        # 准备登录表单数据
        formdata = {
            'username': 'your_username',
            'password': 'your_password',
            'csrf_token': csrf_token
        }
        
        # 提交登录表单
        yield FormRequest.from_response(
            response,
            formdata=formdata,
            callback=self.after_login,
            formxpath='//form[@id="login-form"]'
        )
    
    def after_login(self, response):
        """登录后的处理"""
        # 检查是否登录成功
        if 'authentication failed' in response.text.lower():
            self.logger.error('登录失败')
            return
            
        # 登录成功，开始爬取需要登录才能访问的页面
        yield scrapy.Request('https://example.com/user/dashboard', callback=self.parse_dashboard)
    
    def parse_dashboard(self, response):
        """解析仪表盘页面"""
        # 提取用户数据
        user_info = {
            'username': response.css('div.user-info h3::text').get(),
            'email': response.css('div.user-info p.email::text').get(),
            'last_login': response.css('div.user-info p.last-login::text').get()
        }
        
        yield user_info
        
        # 继续爬取其他需要登录的页面
        order_links = response.css('table.orders tr td a::attr(href)').getall()
        for link in order_links:
            yield response.follow(link, callback=self.parse_order)
    
    def parse_order(self, response):
        """解析订单详情页"""
        order_info = {
            'order_id': response.css('div.order-header span.id::text').get(),
            'date': response.css('div.order-header span.date::text').get(),
            'status': response.css('div.order-status::text').get(),
            'total': response.css('div.order-total::text').get()
        }
        
        # 提取订单项目
        order_items = []
        for item in response.css('table.order-items tr'):
            # 跳过表头行
            if item.css('th'):
                continue
                
            order_items.append({
                'product': item.css('td.product::text').get(),
                'quantity': item.css('td.quantity::text').get(),
                'price': item.css('td.price::text').get()
            })
            
        order_info['items'] = order_items
        yield order_info
        """, language="python")
    
    # 使用Item Loader
    st.subheader("使用Item Loader处理数据")
    
    with st.expander("查看Item Loader示例"):
        st.code("""
import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join
from w3lib.html import remove_tags

class ProductItem(scrapy.Item):
    name = scrapy.Field()
    price = scrapy.Field()
    description = scrapy.Field()
    category = scrapy.Field()
    tags = scrapy.Field()
    rating = scrapy.Field()

class ProductLoader(ItemLoader):
    # 默认输出处理器：取第一个值
    default_output_processor = TakeFirst()
    
    # 名称处理：去除HTML标签和多余空白
    name_in = MapCompose(remove_tags, str.strip)
    
    # 价格处理：去除货币符号，转换为浮点数
    price_in = MapCompose(
        remove_tags, 
        str.strip,
        lambda x: x.replace('$', '').replace(',', '')
    )
    price_out = TakeFirst()
    
    # 描述处理：去除HTML标签，连接多个段落
    description_in = MapCompose(remove_tags, str.strip)
    description_out = Join('\n')
    
    # 类别处理：去除HTML标签和空白
    category_in = MapCompose(remove_tags, str.strip)
    
    # 标签处理：分别处理每个标签
    tags_in = MapCompose(remove_tags, str.strip)
    # 保留所有标签作为列表
    tags_out = lambda x: x
    
    # 评分处理：转换为浮点数
    rating_in = MapCompose(
        remove_tags, 
        str.strip, 
        lambda x: float(x.split('/')[0]) if '/' in x else float(x)
    )

class ProductSpider(scrapy.Spider):
    name = 'product_loader'
    allowed_domains = ['example.com']
    start_urls = ['https://example.com/products']
    
    def parse(self, response):
        # 提取产品链接
        product_links = response.css('div.product-item a::attr(href)').getall()
        for link in product_links:
            yield response.follow(link, self.parse_product)
    
    def parse_product(self, response):
        # 使用ItemLoader加载数据
        loader = ProductLoader(item=ProductItem(), response=response)
        
        loader.add_css('name', 'h1.product-title')
        loader.add_css('price', 'span.price')
        loader.add_css('description', 'div.description p')
        loader.add_css('category', 'ul.breadcrumb li:nth-child(2)')
        loader.add_css('tags', 'div.tags span')
        loader.add_css('rating', 'div.rating span.score')
        
        # 处理最终数据
        yield loader.load_item()
        """, language="python")
    
    # 使用CrawlSpider
    st.subheader("使用CrawlSpider进行通用爬取")
    
    with st.expander("查看CrawlSpider示例"):
        st.code("""
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from myproject.items import ProductItem

class EcommerceSpider(CrawlSpider):
    name = 'ecommerce'
    allowed_domains = ['example.com']
    start_urls = ['https://example.com/shop']
    
    # 定义爬取规则
    rules = (
        # 产品类别页面规则：不获取内容，根据链接继续爬取
        Rule(
            LinkExtractor(
                restrict_css='nav.categories',
                deny=('/login', '/cart', '/checkout')
            ), 
            follow=True
        ),
        
        # 分页规则：不获取内容，跟随链接
        Rule(
            LinkExtractor(
                restrict_css='div.pagination',
                deny=('/login', '/cart', '/checkout')
            ), 
            follow=True
        ),
        
        # 产品详情页规则：提取内容，不跟随链接
        Rule(
            LinkExtractor(
                restrict_css='div.product-list',
                allow=('/product/', '/item/')
            ), 
            callback='parse_product',
            follow=False
        ),
    )
    
    def parse_product(self, response):
        """解析产品详情页"""
        product = ProductItem()
        
        product['name'] = response.css('h1.product-title::text').get()
        product['price'] = response.css('span.price::text').get()
        product['description'] = response.css('div.description::text').get()
        product['category'] = response.css('ul.breadcrumb li:nth-child(2)::text').get()
        product['sku'] = response.css('span.sku::text').get()
        product['availability'] = response.css('span.availability::text').get()
        
        yield product
        """, language="python")
    
    # 实际案例分析
    st.header("实际案例分析")
    
    st.markdown("""
    以下是一个基于模拟的实际案例分析，展示如何使用Scrapy抓取电商网站数据，并进行数据分析。
    """)
    
    # 创建示例分析数据
    df = generate_example_data(100)
    
    # 显示抓取结果
    st.subheader("产品数据抓取结果")
    st.dataframe(df.head(10))
    
    # 分析结果
    st.subheader("数据分析结果")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # 价格分布
        st.write("产品价格分布")
        fig, ax = plt.subplots()
        ax.hist(df['价格'], bins=20)
        ax.set_xlabel('价格')
        ax.set_ylabel('产品数量')
        st.pyplot(fig)
        
        # 类别统计
        st.write("产品类别分布")
        category_counts = df['类别'].value_counts()
        fig, ax = plt.subplots()
        ax.bar(category_counts.index, category_counts.values)
        ax.set_xlabel('类别')
        ax.set_ylabel('产品数量')
        plt.xticks(rotation=45)
        st.pyplot(fig)
    
    with col2:
        # 评分与价格的关系
        st.write("评分与价格的关系")
        fig, ax = plt.subplots()
        ax.scatter(df['价格'], df['评分'])
        ax.set_xlabel('价格')
        ax.set_ylabel('评分')
        st.pyplot(fig)
        
        # 促销产品比例
        st.write("促销产品比例")
        promo_counts = df['是否促销'].value_counts()
        fig, ax = plt.subplots()
        ax.pie(promo_counts, labels=['非促销', '促销'] if promo_counts.index[0] == False else ['促销', '非促销'], 
               autopct='%1.1f%%')
        st.pyplot(fig)
    
    # 常见问题与解决方法
    st.header("常见问题与解决方法")
    
    st.markdown("""
    ### 1. 网站反爬虫措施
    
    网站可能采用多种反爬虫措施，如IP限制、User-Agent检测、Cookie验证、验证码等。
    
    **解决方法**:
    - 控制请求频率（设置适当的DOWNLOAD_DELAY）
    - 使用随机User-Agent中间件
    - 使用代理IP中间件
    - 处理验证码（使用OCR或验证码识别服务）
    - 模拟正常用户行为
    
    ### 2. 动态页面内容
    
    许多现代网站使用JavaScript动态加载内容，Scrapy默认不执行JavaScript。
    
    **解决方法**:
    - 分析网站API，直接请求数据源
    - 使用Splash或Selenium与Scrapy集成
    - 使用scrapy-playwright插件
    
    ### 3. 大规模爬取性能问题
    
    处理大量数据时可能面临性能瓶颈。
    
    **解决方法**:
    - 优化Spider逻辑，减少不必要的请求
    - 调整并发设置（CONCURRENT_REQUESTS）
    - 使用分布式爬取（Scrapy-Redis）
    - 实现增量爬取，只获取新/更新的内容
    
    ### 4. 数据质量和清洗
    
    原始数据可能包含噪声、缺失值或格式不一致的问题。
    
    **解决方法**:
    - 使用Item Pipeline进行数据清洗和验证
    - 利用ItemLoader预处理数据
    - 实现完善的异常处理机制
    """)
    
    # 扩展资源
    st.subheader("扩展资源")
    
    st.markdown("""
    - [Scrapy官方文档](https://docs.scrapy.org/en/latest/)
    - [Scrapy教程](https://docs.scrapy.org/en/latest/intro/tutorial.html)
    - [Scrapy-Splash集成](https://github.com/scrapy-plugins/scrapy-splash)
    - [Scrapy-Selenium集成](https://github.com/clemfromspace/scrapy-selenium)
    - [Scrapy-Redis分布式爬虫](https://github.com/rmax/scrapy-redis)
    """)
    
    # 注意事项
    st.warning("""
    **重要提示**：
    
    在使用爬虫技术时，请务必遵守以下原则：
    
    1. 遵守网站的robots.txt规则
    2. 控制请求频率，避免对服务器造成过大负担
    3. 尊重网站的服务条款
    4. 保护个人隐私数据
    5. 仅用于合法目的，不得用于未授权的数据收集
    
    不当使用爬虫可能导致被屏蔽IP或法律问题。
    """) 