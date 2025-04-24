import scrapy
import datetime
import pymysql
import json
from .num import digit

class Blitem(scrapy.Item):
    ranking = scrapy.Field()
    info = scrapy.Field()
    url = scrapy.Field()
    hot = scrapy.Field()
    uptime = scrapy.Field()

class BlSpider(scrapy.Spider):
    name = 'bl'

    def __init__(self):
        self.conn = pymysql.connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            password='root',
            db='test',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        self.cursor = self.conn.cursor()
 
    def start_requests(self):
        url = f'https://v.api.aa1.cn/api/bilibili-rs/'
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        data = json.loads(response.text)
        count = 1
        for i in data['data'][:30]:
            item = Blitem()
            item['ranking'] = count
            item['info'] = i['title']
            item['url'] = i['link']
            item['hot'] = digit(i['heat'])
            item['uptime'] = datetime.datetime.now()
            count += 1
            sql = """INSERT INTO Bl (ranking, info, url, hot, uptime) VALUES (%s, %s, %s, %s, %s)"""
            self.cursor.execute(sql, (
                item['ranking'],
                item['info'],
                item['url'],
                item['hot'],
                item['uptime']
            ))
            self.conn.commit()
            yield item

    def closed(self, reason):
        self.cursor.close()
        self.conn.close()

