import json
from datetime import datetime

class DoubanMoviesPipeline:
    def __init__(self):
        self.file = None
        self.items = []

    def open_spider(self, spider):
        # 当爬虫开始时创建文件
        filename = f'douban_top250_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        self.file = open(filename, 'w', encoding='utf-8')

    def process_item(self, item, spider):
        # 将item添加到列表中
        self.items.append(dict(item))
        return item

    def close_spider(self, spider):
        # 当爬虫结束时，将所有数据写入文件
        json.dump(self.items, self.file, ensure_ascii=False, indent=2)
        self.file.close()
        print(f"已保存 {len(self.items)} 条电影数据") 