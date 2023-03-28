import scrapy
from scrapy.crawler import CrawlerProcess
import colorama
from colorama import Fore, Back, Style
import re
import sys

GlutenFreeKeyWords = [
  "vete", "gluten", "råg", "korn", "kamut", "dinkel", "vetekli", "kruskakli", "spelt", "durum", "havregryn",
  "mannagryn"
]
re_glutenFreeKeyWords = re.compile("|".join(GlutenFreeKeyWords))
GlutenFree = False


def convertTuple(tup):
  # initialize an empty string
  str = ''
  for item in tup:
    str = str + item + ", "
  return str


class Spider(scrapy.Spider):
  name = "quotes"
  ingredients = ""
  i = 0

  def start_requests(self):
    urls = [input("Input URL please: ")]
    for url in urls:
      yield scrapy.Request(url=url, callback=self.on_response)

  def on_response(self, response):
    i = 0
    while i< 5:
      print(response.xpath("/html/body/div[1]/div/div[1]/div[2]/main/div/div[2]/div/div/div/div[" + str(i) + "]/h2").get())
      i += 1
    #self.CheckForIngredients(response)

  def CheckForIngredients(self, response):
    if response.xpath(
        "/html/body/div[1]/div/div[1]/div[2]/main/div/div[1]/div/div[2]/div[2]/div/div/div/div[1]/div/div/span/text()"
    ).get() == "Glutenfritt":
      print(Fore.GREEN + "Gluten Free")
      print(Style.RESET_ALL)
      GlutenFree = True
      
    if "Ingredienser" in ThirdDiv:
      print("No Ursprungsland")
      ingredients = response.xpath(  "/html/body/div[1]/div/div[1]/div[2]/main/div/div[2]/div/div/div/div[3]/div/text()"
      ).get()
      ingredients = ingredients.lower()
    else:
      if "Ingredienser" in FourthDiv:
        print("Ursprungsland")
        ingredients = response.xpath(   "/html/body/div[1]/div/div[1]/div[2]/main/div/div[2]/div/div/div/div[4]/div/text()"
        ).get()
        ingredients = ingredients.lower()
      else:
        print("No ingredients")
        sys.exit()

    if re_glutenFreeKeyWords.search(ingredients):
      print(Fore.RED + "Not Gluten Free")
      print(Style.RESET_ALL)
      print("Here are the ingredients: " + ingredients)
      print(
        "Here are the marked, potentially gluten containing ingredients: " +
        Fore.RED + convertTuple(re_glutenFreeKeyWords.findall(ingredients)) +
        Style.RESET_ALL)
      GlutenFree = False
    else:
      print(Fore.GREEN + "Gluten free, yay!")
      print(Style.RESET_ALL)
      print("Here are the ingredients: " + ingredients)
      GlutenFree = True


c = CrawlerProcess({
  'USER_AGENT': 'Mozilla/5.0',
  'LOG_LEVEL': 'WARNING',
  'REQUEST_FINGERPRINTER_IMPLEMENTATION': '2.7',
})
c.crawl(Spider)
c.start()
