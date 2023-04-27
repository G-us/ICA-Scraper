import scrapy
from scrapy.crawler import CrawlerProcess
import scrapy_splash
import scrapy_playwright


class Spider(scrapy.Spider):
    ingredients = ""
    name = "ICAScraper"
    i = 0
    productName = ""


    def start_requests(self):
        urls = [
            "https://www.sj.se/kop-resa/valj-resa/Sunne/Karlstad%20C/2023-04-27"
        ]
        for url in urls:
            print("Scraping URL")
            yield scrapy.Request(url=url, meta={"playwright": True}, callback = self.on_response)

    def on_response(self, response):
        print(response.body)
        name = response.xpath(
            "/html/body/main/div/div/div/div[2]/div/div/div[2]/div[1]/article/div/div[2]/div[1]/div[1]/h1"
        ).get()
        print(name)


c = CrawlerProcess({
    'USER_AGENT': 'Mozilla/5.0',
    'LOG_LEVEL': 'WARNING',
    'REQUEST_FINGERPRINTER_IMPLEMENTATION': '2.7',
})

c.crawl(Spider)
c.start()
