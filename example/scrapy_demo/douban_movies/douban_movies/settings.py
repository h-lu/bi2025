BOT_NAME = "douban_movies"

SPIDER_MODULES = ["douban_movies.spiders"]
NEWSPIDER_MODULE = "douban_movies.spiders"

# 遵守robots.txt规则
ROBOTSTXT_OBEY = False

# 配置默认的请求头
DEFAULT_REQUEST_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
}

# 配置下载延迟
DOWNLOAD_DELAY = 2

# 配置并发请求数
CONCURRENT_REQUESTS = 1

# 配置Item Pipeline
ITEM_PIPELINES = {
   "douban_movies.pipelines.DoubanMoviesPipeline": 300,
}

# 启用自动限速
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 5
AUTOTHROTTLE_MAX_DELAY = 60
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0 