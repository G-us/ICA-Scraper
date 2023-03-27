from scrapy.crawler import CrawlerProcess
from spider import Spider

c = CrawlerProcess({
    'USER_AGENT': 'Mozilla/5.0',
    'LOG_LEVEL': 'WARNING',
    'REQUEST_FINGERPRINTER_IMPLEMENTATION': '2.7',
})
c.crawl(Spider)
c.start()