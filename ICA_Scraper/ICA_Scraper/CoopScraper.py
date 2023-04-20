import scrapy
from scrapy.crawler import CrawlerProcess
import scrapy_splash


class Spider(scrapy.Spider):
  ingredients = ""
  name = "ICAScraper"
  i = 0
  productName = ""

  def start_requests(self):
    urls = [
      "https://www.coop.se/handla/varor/mejeri-agg/yoghurt-fil/smaksatt-yoghurt/yoghurt-jordgubb-smultron-7310865018465"
    ]
    for url in urls:
      print("Scraping URL")
      yield scrapy_splash.SplashRequest(url=url, callback=self.on_response)

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
