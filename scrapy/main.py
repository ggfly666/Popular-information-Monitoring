import multiprocessing
import time
import pymysql
from scrapy.crawler import CrawlerProcess
from crawler.wb import WbSpider
from crawler.bl import BlSpider
from crawler.bd import BdSpider

def get_interval_from_db(task_name):
    conn = None
    try:
        conn = pymysql.connect(
            host='127.0.0.1',
            port=3306,
            user='xxx',
            password='xxx',
            db='xxx',  
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        with conn.cursor() as cursor:
            sql = "SELECT * FROM CrawlTime LIMIT 1"
            cursor.execute(sql)
            result = cursor.fetchone()
            if result:
                if task_name == 'wb':
                    return result.get('Wbtime', 12) * 3600  
                elif task_name == 'bl':
                    return result.get('Bltime', 12) * 3600  
                elif task_name == 'bd':
                    return result.get('Bdtime', 12) * 3600  
                else:
                    return 3600  
            else:
                return 3600  
    except Exception as e:
        print(f"Error fetching interval: {e}")
        return 3600 * 12  
    finally:
        if conn:
            conn.close()

def run_spider(spider_class):
    settings = {
        "TELNETCONSOLE_ENABLED": False,
        "LOG_ENABLED": True,
        "LOG_LEVEL": "INFO",
        "LOG_FILE": "scrapy.log",  
    }
    
    process = CrawlerProcess(settings)
    process.crawl(spider_class)
    process.start()  

def schedule_task(task_name, spider_class):
    interval = get_interval_from_db(task_name)
    
    while True:
        run_spider(spider_class)
        time.sleep(interval)  

if __name__ == '__main__':
    processes = []
    for spider_name, spider_class in [
        ('wb', WbSpider),
        ('bl', BlSpider),
        ('bd', BdSpider)
    ]:
        p = multiprocessing.Process(target=schedule_task, args=(spider_name, spider_class))
        p.daemon = True  
        p.start()
        processes.append(p)
    

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        for p in processes:
            p.terminate()