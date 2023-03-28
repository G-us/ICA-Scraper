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
        self.CheckForIngredients(response, headerNumber=self.SearchHeaders(response))

    def SearchHeaders(self, response):
        i = 0
        while i < 10:
            print("At header: " + str(i))
            headerTitle = (response.xpath(
                "/html/body/div[1]/div/div[1]/div[2]/main/div/div[2]/div/div/div/div[" + str(i) + "]/h2").get())
            if headerTitle is None:
                print("No header")
                i += 1
                continue
            elif "Ingredienser" in headerTitle:
                print("Found \"Ingredienser\" in header: " + str(i))
                headerNumber = i
                return headerNumber
                break
            else:
                i += 1
        print("No ingredients")

    def CheckForIngredients(self, response, headerNumber):
        if response.xpath(
                "/html/body/div[1]/div/div[1]/div[2]/main/div/div[1]/div/div[2]/div[2]/div/div/div/div[1]/div/div/span/text()").get() == "Glutenfritt":
            print(Fore.GREEN + "Gluten Free")
            print(Style.RESET_ALL)
            GlutenFree = True

        ingredients = (response.xpath("/html/body/div[1]/div/div[1]/div[2]/main/div/div[2]/div/div/div/div[" + str(
            headerNumber) + "]/div/text()").get())
        ingredients = str(ingredients).lower()

        if re_glutenFreeKeyWords.search(ingredients):
            GlutenFree = False
            self.PrintResult(ingredients, GlutenFree)
        else:
            GlutenFree = True
            self.PrintResult(ingredients, GlutenFree)

    def PrintResult(self, ingredients, GlutenFree):
        if GlutenFree:
            print(Fore.GREEN + "Gluten Free")
            print(Style.RESET_ALL)
            print("Just to make sure, here are the ingredients: " + ingredients)
        else:
            print(Fore.RED + "Not Gluten Free")
            print(Style.RESET_ALL)
            print("Here are the ingredients: " + ingredients)
            print(
                "Here are the marked, potentially gluten containing ingredients: " +
                Fore.RED + convertTuple(re_glutenFreeKeyWords.findall(ingredients)) +
                Style.RESET_ALL)


c = CrawlerProcess({
    'USER_AGENT': 'Mozilla/5.0',
    'LOG_LEVEL': 'WARNING',
    'REQUEST_FINGERPRINTER_IMPLEMENTATION': '2.7',
})
c.crawl(Spider)
c.start()
