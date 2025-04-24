import scrapy
import datetime
import pymysql
import json
from .num import digit

class Bditem(scrapy.Item):
    ranking = scrapy.Field()
    info = scrapy.Field()
    url = scrapy.Field()
    hot = scrapy.Field()
    uptime = scrapy.Field()

class BdSpider(scrapy.Spider):
    name = 'bd'

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
        url = f'https://zj.v.api.aa1.cn/api/baidu-rs/'
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        data = json.loads(response.text)
        for i in data['data'][:30]:
            item = Bditem()
            item['ranking'] = i['index']
            item['info'] = i['title']
            item['url'] = i['url']
            item['hot'] = digit(i['hot'])
            item['uptime'] = datetime.datetime.now()

            sql = """INSERT INTO Bd (ranking, info, url, hot, uptime) VALUES (%s, %s, %s, %s, %s)"""
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

