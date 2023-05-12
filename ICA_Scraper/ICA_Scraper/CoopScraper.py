import re
import sys
import time

import PySimpleGUI as sg
import textwrap3
from colorama import Fore, Style
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import element_to_be_clickable, visibility_of_element_located, \
    visibility_of
from selenium.webdriver.support.wait import WebDriverWait

GlutenFreeKeyWords = [
    "vete", "gluten", "råg", "korn", "kamut", "dinkel", "vetekli", "kruskakli", "spelt", "durum", "havregryn",
    "mannagryn"
]

LactoseKeyWords = [
    "mjölk", "mjölkprotein", "mjölkproteinhydrolysat", "mjölkproteinisolat", "mjölkproteinkoncentrat", "laktose",
    "grädde", "smör", "ost"
]

DeezNutsKeyWords = ["nöt", "jordnöt", "mandel", "cashewnöt", "hasselnöt", "valnöt", "pistagenöt", "pecannöt",
                    "macadamianöt", "paranöt", "kastanjenöt"]
re_SelectedKeyWords = []

SubmitImage = b'iVBORw0KGgoAAAANSUhEUgAAADIAAAAyCAYAAAAeP4ixAAAACXBIWXMAAAsTAAALEwEAmpwYAAAEN0lEQVRoge3YW4hVVRzH8c+a8VKaWg6Wgr2UURIS6tGJSEYjMiuDXgyjnrq+SChIZUgRdIHAqAyiG0UvaU9lkBdQCy+lM2NjPkZaLyppalpoOmf1sM9pduPsc87ex4EJ5vu0zjpr/X/7t9dl/9dimGGGGeb/RGg2wA7GXU5HpD0wLdIWacEpHAp0ldk6lyPNP242hY10Mgsr8ADG1Gl+IbK9hTdn81VRzVrkNrKTq0ezJrC08ubzELEr8tQcDuTVrkUuI13Mi6zDlH5/HY9sD/QEjpTpDUwMTI904Lq0VuRsYFmJD5q3kNCwkb3cj3WBy1LV3ZFXDrJhCX9n9e2kPbIyJNOwOooRL5Z4qdCT96MhI13MK7O5aqLyRp+ZzdpAuVGxLu6IfIxrK1URT5d4O++D96eukW4mlenRN51ORu6bw84igj9yzTm+xsxK1fleOtrZXSRelbqLtcwb+kycxeKiJmAGR3EXfqpUjWzlw05GFo1JHSOdzAosTVU9W2JHM4JQ4lhkib51NR2PNhOz3oisqG6xkR9+Zm0zYmnmsC/wTqpq+Qv5t/N/yVwjB7jibDINxlQaPjib9UWFBqIzmbIHMRqxzO1z2VUkVuYbOMd8fSZOHOWLIgK1KHE4srnyM7SwqGisTCO9tFfLZb69h3NFRepQNSKmNPOSaSQwLVXuKSpQj8j+gTTzUstIW7VcTtbKoBD/mxVPVDCRzTSSTggDvUWCN0JvKjOItMSCcWptd6dSjdpqtGuKUanYgT9CkrbkptbUOlQtl5MP1mBxU6p8sGiQWka6Uz874iU4TWawIFXuzmxVh1prZGusrI3A1H3MKyqSxSbGhuR4oKKzpWisTCMlDge+qWqUWVlUJIs2HotcVfn52/jBMAKRt/Qtvnu7m/jy9mcPk7E6pfXeDU18dGsaKfFloglCLx99x9SiYlW2MSLwqb4d69h51jQTs6aRQGzhSZU3FZg8go2dF5/ZG2YbI8bxSeDOlM6q2/i9aEwaSJtnJenJCn1T7Gbs7uLWvGKdTBmfnA4fSteXeXwfV+aNl6bhLbWLlyPPVftELgTex2slfq3Vt3IkeCLyfEjSkIHY08rCmZxs+OlT5Po27E12rlcDranq89iKzWX2j+LwBXojbdXroMBiTGhAorCZ3B+5vcyvjETRTPUEVkmOugsG+L+QmdxHyzlsP82MwHL8kqPricjrLdxY4t2RyShtG6Dd3F425V0zTaUd62m9PklfFkkORdMwIdISOB0rl9iBLZGNJf5K9+9h7Hk2uAQjc8nzp/W0TiIs4EIj7Tcxti3DTGTPGRYuaMDMYCWCubgUZoaEEZo3M2SMUHfNfH+au7PMFL4QGwxu4c/j2btZ+ziWZfUdUiNSZaBpFvmsxMNZ9wdDakSqLLx4ZD4/wyODeQkyqPQwtpPVzd7UDzPMMMMMPf4BTrogPAcmKlcAAAAASUVORK5CYII='
ExitImage = b'iVBORw0KGgoAAAANSUhEUgAAADIAAAAyCAYAAAAeP4ixAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAEkUlEQVR4Xr2az08TQRTHF0TS8rOoiQcvRq96QKPhpsYD/4ExMQjbtBAxEAjBiweVg4nhoCeVGIMJB00sbSEQCPKrUAoXT578CzCgiAkY+aHP93botoXdzuzMtE02admZN+8z35k382YwDM4Henr6YXz8Oq9cId9De3tQ2j7s7ZWggUEwDIDKSoCxsUZpYwoVoaLih+VDOHzHsxnY3T0OodCAZSD9VFTsQCzm3Zjn1lkFbKsK/P7vOT6Y5lNhcwhRhhBvcwykYfz+bRgZCQsbkyyIbZxEiA1HH0KhV1yzCFECpjnkaCADswXDww+4xiQLoBLnXSHSPpjmYF7zqEQsL0TakM+3jQ12SfrqWg2VuIwQm0I+hEJPHA2hEhNCBjLK/IZIpFcXDESjTTixdz35YJq57UNr62tPBjLKAMTjD1VhYHS0D5XIBJbsIMP7Hg53sujQ3d0rBZENE4m8kIVBJSalIZgP/6Cz8waDqatbV4Kh3ozHB7zC4Jz4qggBEAh8y2kX/6AG4/MBzpmoKAwGiw3tEJYqyeRZhMldgHjj8/B7UiYW+8yDQSVAA8Qv9/CXSl1BGLYlkH1ImeFhrO78QVB1iNraXex4f/61JJlsRJgtaRDqAIIhhwEupRvD7xe0KFFbC7CwUM9TnU3+VKoJA8COEgwNs0iEYBrwqcfoBLhOyCtNHRQIACwt3RKCsHtwcfGRVVF2iKWViccB1wkdwwkgkXjsCcKGWV5+rgxTXg5Aj0qH0HBKpd5JQWQpE8VhpuaIKkQisaEEYcOkUkPKysjAsDnhGgGl4GBx8X1RlSGIhQW9EFnKvCmKMgSRTBYGwoZJJj8VFIatE4WFyFLmS0GGWSHmBG8iofSrWpUhiESCFtAyXtva38PKCkBVlXpopuMmjE74yb9/ykNQKkuHjZYaa2uGsbcnayJTb3/fMNbX6be0P9JOWHsn2fTUaU1h+UxxJrk92SmfUN0AOsGwfKY4MFryiXyrPCefkR5C2RW15BMiW5WDfEaL04eNFFwJp7Q5EtnUClM0JQ7DkDLxeJ8WGO3RSWRoZZdhmeZdJRgtmZ2OxIopc1sKRosS7IIIYGJCfQfA1plWTzDWnFBdJ2jrQgAA5/A5BVNTANXVatsZts6EhGC0RCdyeGbGOkGxF1GAqzA3B1BTowbD1pn7eWFQiTnlbQc5Oj1NEKePhHCAEzA7qwcmGnW+IKX7QWUISopwK86TnhInoLJeI1h2eTZn7h1pSwvE/DwXwh5qBKPj3CwWu2nD4MReVeodyRwbz6pAOdNk60yJBYMQf6RBBIeT23DD0xl1Zdra2OUoXsafQZC/nmHYCaDwcHKFWV6WhwkGc9vHy9AuTyAHOTZvYou+t5TxeqLZ3OzciXg9/VEIhpTQfQJII4PmjGgAQCXw/wKOuXYUKjOZF4adOw2J9rTXcng685ML09JCEPzTFlTmgyMMi05qO1EBMlTmmSsMU4IPYcd503yZA8POYq8J+KGlCHZYwxEYtznBaxGjWb8Fw04AL/LKF+K9HQCCwVkl+3gZ34tKBJSMKFaGjg7ucP4Pc7yAommR+nUAAAAASUVORK5CYII='

TextFont = ("Noto Sans", 15)
IngredientsFont = ("Noto Sans", 12)
WrapSize = 70
ImgSize = (50, 50)

Product_Ingredients = ""
Product_Name = ""

chrome_options = Options()

chrome_options.add_argument("--headless=new")

InputURL = "https://www.coop.se/handla/varor/skafferi/pasta-pastasas/formpasta/pasta-farfalle-8076808060654"

layout = [[sg.OptionMenu(values=('Gluten', 'Lactose', 'Deez Nuts'), k='-KEYWORDS-', default_value='Gluten')],
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


def getIngredients():
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
        re_SelectedKeyWords = re.compile("|".join(DeezNutsKeyWords))
    # End program if user closes window or
    # presses the OK button
    if event == sg.WIN_CLOSED or event == '-EXIT-':
        sys.exit()
    elif event == '-SUBMIT-':
        getIngredients()
