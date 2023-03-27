import scrapy

class Spider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        urls = [    'https://handlaprivatkund.ica.se/stores/1004584/products/Bryggkaffe-Mellanrost-500g-Arvid-Nordquist-Classic/1004503',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.on_response)

    def on_response(self, response):

      ThirdDiv = response.xpath("/html/body/div[1]/div/div[1]/div[2]/main/div/div[2]/div/div/div/div[3]/h2").get()
      if ThirdDiv.___contains___("Ingredienser"):
        
        print("No Ursprungsland")
        ingredients = response.xpath("/html/body/div[1]/div/div[1]/div[2]/main/div/div[2]/div/div/div/div[3]/div/text()").get()
      else:
        print("Ursprungsland")
        ingredients = response.xpath("/html/body/div[1]/div/div[1]/div[2]/main/div/div[2]/div/div/div/div[4]/div/text()").get()

      print("This is the 3 header: " + response.xpath("/html/body/div[1]/div/div[1]/div[2]/main/div/div[2]/div/div/div/div[3]/h2/text").get())
      print(ingredients)

      
      