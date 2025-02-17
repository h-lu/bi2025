import scrapy
from scrapy.http import Request

class DoubanMoviesSpider(scrapy.Spider):
    name = 'douban_movies'
    allowed_domains = ['movie.douban.com']
    base_url = 'https://movie.douban.com/top250'
    
    custom_settings = {
        'ROBOTSTXT_OBEY': False,
        'DOWNLOAD_DELAY': 2,
        'COOKIES_ENABLED': False,
        'DEFAULT_REQUEST_HEADERS': {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        }
    }

    def start_requests(self):
        # 生成所有页面的URL
        for i in range(10):
            url = f'{self.base_url}?start={i*25}'
            yield Request(url=url, callback=self.parse, meta={'page': i+1})

    def parse(self, response):
        page = response.meta['page']
        print(f'正在爬取第{page}页...')
        
        # 获取当前页面所有电影条目
        movie_items = response.css('ol.grid_view li')
        
        for item in movie_items:
            movie = {}
            
            # 电影标题
            movie['title'] = item.css('span.title::text').get('')
            
            # 基本信息
            info = item.css('div.bd p:first-child::text').getall()
            info = [i.strip() for i in info if i.strip()]
            if info:
                # 导演和主演
                movie['director'] = info[0].split('导演: ')[-1].split('主演:')[0].strip()
                
                # 年份、国家、类型
                if len(info) > 1:
                    other_info = info[1].split('/')
                    movie['year'] = other_info[0].strip()
                    movie['country'] = other_info[1].strip() if len(other_info) > 1 else ''
                    movie['genre'] = other_info[2].strip() if len(other_info) > 2 else ''
            
            # 评分
            movie['rating'] = item.css('span.rating_num::text').get('')
            
            # 评价人数
            movie['rating_people'] = item.css('div.star span:last-child::text').re_first(r'(\d+)人评价', '')
            
            # 一句话评价
            movie['quote'] = item.css('span.inq::text').get('')
            
            yield movie 