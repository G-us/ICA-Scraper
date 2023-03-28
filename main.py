import scrapy
from scrapy.crawler import CrawlerProcess
import colorama
from colorama import Fore, Back, Style
import re
from scrapy import exceptions
import PySimpleGUI as sg
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
    ingredients = ""
    name = "ICAScraper"
    i = 0
    productName = ""




    def start_requests(self):
        urls = [InputURL]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.on_response)

    def on_response(self, response):
        self.CheckForIngredients(response, headerNumber=self.SearchHeaders(response))

    def SearchHeaders(self, response):
        global productName
        productName = (response.xpath(
            "/html/body/div[1]/div/div[1]/div[2]/main/div/div[1]/div/div[2]/div/div[1]/h1/text()").get())
        i = 0
        while i < 10:
            headerTitle = (response.xpath(
                "/html/body/div[1]/div/div[1]/div[2]/main/div/div[2]/div/div/div/div[" + str(i) + "]/h2").get())
            if headerTitle is None:
                i += 1
                continue
            elif "Ingredienser" in headerTitle:
                print("Found \"Ingredienser\" in header: " + str(i))
                headerNumber = i
                return headerNumber
                break
            else:
                i += 1
        print(Style.BRIGHT + Fore.RED + "NO INGREDIENTS FOUND")
        raise scrapy.exceptions.CloseSpider("No ingredients found")

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
        print(Style.BRIGHT + Fore.BLUE + "Product: " + Fore.YELLOW + productName + Style.RESET_ALL)
        if GlutenFree:
            print(Fore.BLUE + "Result: " + Fore.GREEN + "Gluten Free")
            print(Style.RESET_ALL)
            print("Just to make sure, here are the ingredients: " + ingredients)
            window['-OUTPUT-'].update('Gluten Free')
            window["Again"].update(visible=True, disabled=False)
            window.finalize()
        else:
            print(Fore.BLUE + "Result: " + Fore.RED + "Not Gluten Free")
            print(Style.RESET_ALL)
            print("Here are the ingredients: " + ingredients)
            print(
                "Here are the marked, potentially gluten containing ingredients: " +
                Fore.RED + convertTuple(re_glutenFreeKeyWords.findall(ingredients)) +
                Style.RESET_ALL)
            window['-OUTPUT-'].update('Not Gluten Free')
            window["Again"].update(visible=True, disabled=False)
            window.finalize()



c = CrawlerProcess({
    'USER_AGENT': 'Mozilla/5.0',
    'LOG_LEVEL': 'WARNING',
    'REQUEST_FINGERPRINTER_IMPLEMENTATION': '2.7',
})


while True:
    layout = [[sg.Text("Input Link")],
              [sg.Input(key='-INPUT-', do_not_clear=False)],
              [sg.Text(size=(40, 1), key='-OUTPUT-')],
              [sg.Button('Submit'), sg.Button('Quit')],
              [sg.Button('Again', disabled=True, visible=False)]]

    window = sg.Window('Gluten Free Checker', layout)
    event, values = window.read()
    global InputURL
    InputURL = values["-INPUT-"]
    # End program if user closes window or
    # presses the OK button
    if event == sg.WIN_CLOSED or event == 'Quit':
        sys.exit()
    elif event == 'Submit':
        print(InputURL)
        c.crawl(Spider)
        c.start()
    elif event == "Again":
        print("Again")
        window['-OUTPUT-'].update('hello')

