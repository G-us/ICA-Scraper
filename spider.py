import scrapy

class Spider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        urls = [    'https://handlaprivatkund.ica.se/stores/1004584/products/Kalkon-R%C3%B6kt-tunna-skivor-200g-P%C3%A4rsons/1026006',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.on_response)

    def on_response(self, response):

      ThirdDiv = response.xpath("/html/body/div[1]/div/div[1]/div[2]/main/div/div[2]/div/div/div/div[3]/h2").get()
      if "Ingredienser" in ThirdDiv:
        
        print("No Ursprungsland")
        ingredients = response.xpath("/html/body/div[1]/div/div[1]/div[2]/main/div/div[2]/div/div/div/div[3]/div/text()").get()
      else:
        print("Ursprungsland")
        ingredients = response.xpath("/html/body/div[1]/div/div[1]/div[2]/main/div/div[2]/div/div/div/div[4]/div/text()").get()

      print(ingredients)

      
      