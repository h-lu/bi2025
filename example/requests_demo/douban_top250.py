import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random

class DoubanMovieCrawler:
    def __init__(self):
        self.base_url = "https://movie.douban.com/top250"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
        }
        self.movies = []

    def get_page(self, page=0):
        """获取单页电影数据"""
        url = f"{self.base_url}?start={page*25}"
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"获取页面失败: {e}")
            return None

    def parse_page(self, html):
        """解析页面内容"""
        if not html:
            return
        
        soup = BeautifulSoup(html, 'html.parser')
        movie_list = soup.find('ol', class_='grid_view')
        
        if not movie_list:
            return
        
        for movie_item in movie_list.find_all('li'):
            try:
                movie = {}
                
                # 电影标题
                title_element = movie_item.find('span', class_='title')
                movie['title'] = title_element.text if title_element else ''
                
                # 基本信息
                bd_element = movie_item.find('div', class_='bd')
                if bd_element:
                    info = bd_element.find('p', class_='').text.strip()
                    info_parts = info.split('\n')
                    movie['director'] = info_parts[0].split('导演: ')[-1].split('主演:')[0].strip()
                    movie['year'] = info_parts[1].strip().split('/')[0].strip()
                    movie['country'] = info_parts[1].strip().split('/')[-2].strip()
                    movie['genre'] = info_parts[1].strip().split('/')[-1].strip()
                
                # 评分
                rating_element = movie_item.find('span', class_='rating_num')
                movie['rating'] = rating_element.text if rating_element else ''
                
                # 评价人数
                rating_people = movie_item.find('div', class_='star').find_all('span')[-1]
                movie['rating_people'] = rating_people.text[:-3] if rating_people else ''
                
                # 一句话评价
                quote_element = movie_item.find('span', class_='inq')
                movie['quote'] = quote_element.text if quote_element else ''
                
                self.movies.append(movie)
                
            except Exception as e:
                print(f"解析电影信息时出错: {e}")
                continue

    def crawl(self):
        """爬取所有页面"""
        for i in range(10):  # 豆瓣Top250共10页
            print(f"正在爬取第{i+1}页...")
            html = self.get_page(i)
            self.parse_page(html)
            # 添加随机延时，避免被封IP
            time.sleep(random.uniform(1, 3))
        
        return self.movies

    def save_to_csv(self, filename='douban_top250.csv'):
        """保存数据到CSV文件"""
        if self.movies:
            df = pd.DataFrame(self.movies)
            df.to_csv(filename, index=False, encoding='utf-8-sig')
            print(f"数据已保存到 {filename}")

def main():
    crawler = DoubanMovieCrawler()
    crawler.crawl()
    crawler.save_to_csv()

if __name__ == "__main__":
    main() 