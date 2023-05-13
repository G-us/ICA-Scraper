import re
import sys
import time

import PySimpleGUI as sg
import textwrap3
from colorama import Fore, Style
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import element_to_be_clickable, visibility_of_element_located
from selenium.webdriver.support.wait import WebDriverWait

GlutenFreeKeyWords = [
    "vete", "gluten", "råg", "korn", "kamut", "dinkel", "vetekli", "kruskakli", "spelt", "durum", "havregryn",
    "mannagryn"
]

LactoseKeyWords = [
    "mjölk", "mjölkprotein", "mjölkproteinhydrolysat", "mjölkproteinisolat", "mjölkproteinkoncentrat", "laktose",
    "grädde", "smör", "ost"
]

NutsKeyWords = ["nöt", "jordnöt", "mandel", "cashewnöt", "hasselnöt", "valnöt", "pistagenöt", "pecannöt",
                    "macadamianöt", "paranöt", "kastanjenöt"]
re_SelectedKeyWords = []

SubmitImage = b'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'
ExitImage = b'iVBORw0KGgoAAAANSUhEUgAAADIAAAAyCAYAAAAeP4ixAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAEkUlEQVR4Xr2az08TQRTHF0TS8rOoiQcvRq96QKPhpsYD/4ExMQjbtBAxEAjBiweVg4nhoCeVGIMJB00sbSEQCPKrUAoXT578CzCgiAkY+aHP93botoXdzuzMtE02admZN+8z35k382YwDM4Henr6YXz8Oq9cId9De3tQ2j7s7ZWggUEwDIDKSoCxsUZpYwoVoaLih+VDOHzHsxnY3T0OodCAZSD9VFTsQCzm3Zjn1lkFbKsK/P7vOT6Y5lNhcwhRhhBvcwykYfz+bRgZCQsbkyyIbZxEiA1HH0KhV1yzCFECpjnkaCADswXDww+4xiQLoBLnXSHSPpjmYF7zqEQsL0TakM+3jQ12SfrqWg2VuIwQm0I+hEJPHA2hEhNCBjLK/IZIpFcXDESjTTixdz35YJq57UNr62tPBjLKAMTjD1VhYHS0D5XIBJbsIMP7Hg53sujQ3d0rBZENE4m8kIVBJSalIZgP/6Cz8waDqatbV4Kh3ozHB7zC4Jz4qggBEAh8y2kX/6AG4/MBzpmoKAwGiw3tEJYqyeRZhMldgHjj8/B7UiYW+8yDQSVAA8Qv9/CXSl1BGLYlkH1ImeFhrO78QVB1iNraXex4f/61JJlsRJgtaRDqAIIhhwEupRvD7xe0KFFbC7CwUM9TnU3+VKoJA8COEgwNs0iEYBrwqcfoBLhOyCtNHRQIACwt3RKCsHtwcfGRVVF2iKWViccB1wkdwwkgkXjsCcKGWV5+rgxTXg5Aj0qH0HBKpd5JQWQpE8VhpuaIKkQisaEEYcOkUkPKysjAsDnhGgGl4GBx8X1RlSGIhQW9EFnKvCmKMgSRTBYGwoZJJj8VFIatE4WFyFLmS0GGWSHmBG8iofSrWpUhiESCFtAyXtva38PKCkBVlXpopuMmjE74yb9/ykNQKkuHjZYaa2uGsbcnayJTb3/fMNbX6be0P9JOWHsn2fTUaU1h+UxxJrk92SmfUN0AOsGwfKY4MFryiXyrPCefkR5C2RW15BMiW5WDfEaL04eNFFwJp7Q5EtnUClM0JQ7DkDLxeJ8WGO3RSWRoZZdhmeZdJRgtmZ2OxIopc1sKRosS7IIIYGJCfQfA1plWTzDWnFBdJ2jrQgAA5/A5BVNTANXVatsZts6EhGC0RCdyeGbGOkGxF1GAqzA3B1BTowbD1pn7eWFQiTnlbQc5Oj1NEKePhHCAEzA7qwcmGnW+IKX7QWUISopwK86TnhInoLJeI1h2eTZn7h1pSwvE/DwXwh5qBKPj3CwWu2nD4MReVeodyRwbz6pAOdNk60yJBYMQf6RBBIeT23DD0xl1Zdra2OUoXsafQZC/nmHYCaDwcHKFWV6WhwkGc9vHy9AuTyAHOTZvYou+t5TxeqLZ3OzciXg9/VEIhpTQfQJII4PmjGgAQCXw/wKOuXYUKjOZF4adOw2J9rTXcng685ML09JCEPzTFlTmgyMMi05qO1EBMlTmmSsMU4IPYcd503yZA8POYq8J+KGlCHZYwxEYtznBaxGjWb8Fw04AL/LKF+K9HQCCwVkl+3gZ34tKBJSMKFaGjg7ucP4Pc7yAommR+nUAAAAASUVORK5CYII='
COOPGreen = {'BACKGROUND': '#ffffff',
          'TEXT': '#0a893d',
          'INPUT': '#ffffff',
          'TEXT_INPUT': '#0a893d',
          'SCROLL': '#505F69',
          'BUTTON': ('#0a893d', '#00a142'),
          'PROGRESS': ('#505F69', '#32414B'),
          'BORDER': 1, 'SLIDER_DEPTH': 0, 'PROGRESS_DEPTH': 0,
          }
TextFont = ("Noto Sans", 15)
IngredientsFont = ("Noto Sans", 12)
WrapSize = 70
ImgSize = (50, 50)

sg.theme_add_new('COOPGreen', COOPGreen)
sg.theme('COOPGreen')  # Add a touch of color
Product_Ingredients = ""
Product_Name = ""

chrome_options = Options()

chrome_options.add_argument("--headless=new")


layout = [[sg.OptionMenu(values=('Gluten', 'Lactose', 'Nuts'), k='-KEYWORDS-', default_value='Gluten')],
          [sg.Text("Input Link", text_color='black')],
          [sg.Input(key='-INPUT-', do_not_clear=False)],
          [sg.Text(key="-PRODUCTNAME-", border_width=0, pad=0, text_color="black"),
           sg.Text(key='-ALLERGENSTATUS-', border_width=0, pad=0)],
          [sg.Text(key="-INGREDIENTS-", border_width=0, pad=0, font=IngredientsFont, text_color='black'),
           sg.Image(key="-IMAGE-", pad=0)],
          [sg.Text(key="-ALLERGENS-", border_width=0, pad=0, font=IngredientsFont, text_color='red')],
          [sg.Button('', image_data=SubmitImage, image_size=(50, 50), key="-SUBMIT-", border_width=0),
           sg.Button('', image_data=ExitImage, image_size=(50, 50), key="-EXIT-", border_width=0)]]

window = sg.Window('Gluten Free Checker', layout, font=TextFont)


def convertTuple(tup):
    # initialize an empty string
    str = ''
    for item in tup:
        str = str + item + ", "
    return str


def getImage(driver):
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
    time.sleep(5)
    with open('DownloadedImages/ProductImage.png', 'wb') as file:
        I = driver.find_element(By.CLASS_NAME, "ZDGqWGZP")
        file.write(I.screenshot_as_png)


def getIngredients(InputURL):
    driver = webdriver.Chrome(options=chrome_options)
    if InputURL == "":
        url = "https://www.coop.se/handla/varor/mejeri-agg/mellanmal-dessert/kylda-smamal/risifrutti-jordgubb-7310090771623"

    else:
        url = InputURL
    print("Starting search at url: " + url)
    driver.get(url)
    driver.delete_all_cookies()
    ## Finding Elements
    WebDriverWait(driver, 10).until(element_to_be_clickable((By.ID, "cmpbntyestxt")))
    CookiesBtn = driver.find_element(By.ID, "cmpbntyestxt")
    CookiesBtn.click()
    WebDriverWait(driver, 10).until(element_to_be_clickable((By.XPATH,
                                                             "/html/body/main/div/div/div/div[2]/div/div/div[2]/div[1]/article/div/div[2]/div[3]/div/div[2]/div/div[1]/button")))
    Product_Button = driver.find_element(By.CLASS_NAME,
                                         "LurWyzpq")
    Product_Button.click()
    WebDriverWait(driver, 10).until(visibility_of_element_located((By.CSS_SELECTOR,
                                                                   "#Produktfakta > div:nth-child(1) > div:nth-child(1) > div:nth-child(2)")))
    Product_Ingredients = driver.find_element(By.CSS_SELECTOR,
                                              "#Produktfakta > div:nth-child(1) > div:nth-child(1) > div:nth-child(2)").text
    Product_Name = driver.find_element(By.CLASS_NAME, "ItemInfo-heading").text
    print(Product_Ingredients)
    print(Product_Name)


    getImage(driver)
    CheckForIngredients(Product_Ingredients, Product_Name)


def CheckForIngredients(ingredients, name):
    ingredients = str(ingredients).lower()
    ingredients = textwrap3.fill(ingredients, WrapSize)

    if re_SelectedKeyWords.search(ingredients):
        detectedAllergens = re_SelectedKeyWords.findall(ingredients)
        AllergenFree = False
        PrintResult(ingredients, AllergenFree, name)
    else:
        detectedAllergens = re_SelectedKeyWords.findall(ingredients)
        AllergenFree = True
        PrintResult(ingredients, AllergenFree, name)


def PrintResult(ingredients, AllergenFree, name):
    print(Style.BRIGHT + Fore.BLUE + "Product: " + Fore.YELLOW + name + Style.RESET_ALL)
    if AllergenFree:
        print(Fore.BLUE + "Result: " + Fore.GREEN + values['-KEYWORDS-'] + " Free")
        print(Style.RESET_ALL)
        print("Just to make sure, here are the ingredients: " + ingredients)
        window['-PRODUCTNAME-'].update(name + " is ")
        window['-ALLERGENSTATUS-'].update(values['-KEYWORDS-'] + " free!", text_color='green')
        window['-INGREDIENTS-'].update("Ingredients: " + ingredients)
    else:
        print(Fore.BLUE + "Result: " + Fore.RED + "not " + (values['-KEYWORDS-'].lower()) + " free")
        print(Style.RESET_ALL)
        print("Here are the ingredients: " + ingredients)
        print(
            "Here are the marked, potentially " + (values['-KEYWORDS-'].lower()) + " containing ingredients: " +
            Fore.RED + convertTuple(re_SelectedKeyWords.findall(ingredients)) +
            Style.RESET_ALL)
        window['-PRODUCTNAME-'].update(name + " is ")
        window['-ALLERGENSTATUS-'].update("not " + (values['-KEYWORDS-'].lower()) + " free", text_color='red')
        window['-INGREDIENTS-'].update("Ingredients: " + ingredients)
        window['-ALLERGENS-'].update("Allergens: " + convertTuple(re_SelectedKeyWords.findall(ingredients)))


while True:
    event, values = window.read()
    InputURL = values["-INPUT-"]
    if values["-KEYWORDS-"] == "Gluten":
        re_SelectedKeyWords = re.compile("|".join(GlutenFreeKeyWords))
        AllergenFree = False
    elif values["-KEYWORDS-"] == "Lactose":
        re_SelectedKeyWords = re.compile("|".join(LactoseKeyWords))
        AllergenFree = False
    elif values["-KEYWORDS-"] == "Deez Nuts":
        re_SelectedKeyWords = re.compile("|".join(NutsKeyWords))
    # End program if user closes window or
    # presses the OK button
    if event == sg.WIN_CLOSED or event == '-EXIT-':
        sys.exit()
    elif event == '-SUBMIT-':
        getIngredients()
