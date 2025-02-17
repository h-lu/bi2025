from playwright.sync_api import sync_playwright
import pandas as pd
import time
import random
import json
from datetime import datetime

class JDCrawler:
    def __init__(self):
        self.products = []
        self.base_url = "https://search.jd.com/Search"
        
    def search_products(self, keyword, page_count=2):
        """
        搜索商品并获取数据
        :param keyword: 搜索关键词
        :param page_count: 要爬取的页数
        """
        with sync_playwright() as p:
            # 启动浏览器
            browser = p.chromium.launch(headless=False)
            context = browser.new_context()
            page = context.new_page()
            
            for page_num in range(page_count):
                try:
                    # 构造URL
                    url = f"{self.base_url}?keyword={keyword}&page={2*page_num+1}"
                    print(f"正在爬取第{page_num+1}页: {url}")
                    
                    # 访问页面
                    page.goto(url)
                    # 等待商品列表加载完成
                    page.wait_for_selector('.gl-item')
                    # 模拟滚动到底部以加载所有商品
                    page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
                    time.sleep(random.uniform(1, 2))
                    
                    # 获取商品列表
                    items = page.query_selector_all('.gl-item')
                    
                    for item in items:
                        try:
                            product = {}
                            
                            # 商品标题
                            title_element = item.query_selector('.p-name em')
                            product['title'] = title_element.inner_text() if title_element else ''
                            
                            # 商品价格
                            price_element = item.query_selector('.p-price strong i')
                            product['price'] = price_element.inner_text() if price_element else ''
                            
                            # 商品ID
                            product['id'] = item.get_attribute('data-sku')
                            
                            # 店铺名称
                            shop_element = item.query_selector('.p-shop a')
                            product['shop'] = shop_element.get_attribute('title') if shop_element else ''
                            
                            # 评论数
                            comment_element = item.query_selector('.p-commit strong a')
                            product['comments'] = comment_element.inner_text() if comment_element else ''
                            
                            self.products.append(product)
                            
                        except Exception as e:
                            print(f"解析商品数据时出错: {e}")
                            continue
                    
                    # 随机延时
                    time.sleep(random.uniform(2, 4))
                    
                except Exception as e:
                    print(f"爬取页面时出错: {e}")
                    continue
            
            # 关闭浏览器
            browser.close()
    
    def save_to_csv(self, filename=None):
        """保存数据到CSV文件"""
        if not filename:
            filename = f'jd_products_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        
        if self.products:
            df = pd.DataFrame(self.products)
            df.to_csv(filename, index=False, encoding='utf-8-sig')
            print(f"数据已保存到 {filename}")
    
    def save_to_json(self, filename=None):
        """保存数据到JSON文件"""
        if not filename:
            filename = f'jd_products_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        
        if self.products:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.products, f, ensure_ascii=False, indent=2)
            print(f"数据已保存到 {filename}")

def main():
    # 创建爬虫实例
    crawler = JDCrawler()
    
    # 搜索并爬取商品数据
    keyword = "笔记本电脑"
    crawler.search_products(keyword, page_count=2)
    
    # 保存数据
    crawler.save_to_csv()
    crawler.save_to_json()

if __name__ == "__main__":
    main() 