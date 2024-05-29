#!/usr/bin/env python
import random

import PySimpleGUI as sg
from CoopScraper import SearchCOOP
import re
from ICAScraper import SearchICA
import textwrap3
from colorama import Fore, Style
from ctypes import windll
from PIL import Image
import json
windll.shcore.SetProcessDpiAwareness(1)


productImageDir = r"C:\Users\HenryParsons\PycharmProjects\SafeBites\productImage.png"

dataSet = {
    "AllergenStatus": False,
    "Ingredients": "",
    "DetectedAllergens": "",
    "ProductTitle": ""

}

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

customKeyWords = []
re_SelectedKeyWords = []

SubmitImage = b'iVBORw0KGgoAAAANSUhEUgAAADIAAAAyCAYAAAAeP4ixAAAACXBIWXMAAAsTAAALEwEAmpwYAAAEN0lEQVRoge3YW4hVVRzH8c+a8VKaWg6Wgr2UURIS6tGJSEYjMiuDXgyjnrq+SChIZUgRdIHAqAyiG0UvaU9lkBdQCy+lM2NjPkZaLyppalpoOmf1sM9pduPsc87ex4EJ5vu0zjpr/X/7t9dl/9dimGGGGeb/RGg2wA7GXU5HpD0wLdIWacEpHAp0ldk6lyPNP242hY10Mgsr8ADG1Gl+IbK9hTdn81VRzVrkNrKTq0ezJrC08ubzELEr8tQcDuTVrkUuI13Mi6zDlH5/HY9sD/QEjpTpDUwMTI904Lq0VuRsYFmJD5q3kNCwkb3cj3WBy1LV3ZFXDrJhCX9n9e2kPbIyJNOwOooRL5Z4qdCT96MhI13MK7O5aqLyRp+ZzdpAuVGxLu6IfIxrK1URT5d4O++D96eukW4mlenRN51ORu6bw84igj9yzTm+xsxK1fleOtrZXSRelbqLtcwb+kycxeKiJmAGR3EXfqpUjWzlw05GFo1JHSOdzAosTVU9W2JHM4JQ4lhkib51NR2PNhOz3oisqG6xkR9+Zm0zYmnmsC/wTqpq+Qv5t/N/yVwjB7jibDINxlQaPjib9UWFBqIzmbIHMRqxzO1z2VUkVuYbOMd8fSZOHOWLIgK1KHE4srnyM7SwqGisTCO9tFfLZb69h3NFRepQNSKmNPOSaSQwLVXuKSpQj8j+gTTzUstIW7VcTtbKoBD/mxVPVDCRzTSSTggDvUWCN0JvKjOItMSCcWptd6dSjdpqtGuKUanYgT9CkrbkptbUOlQtl5MP1mBxU6p8sGiQWka6Uz874iU4TWawIFXuzmxVh1prZGusrI3A1H3MKyqSxSbGhuR4oKKzpWisTCMlDge+qWqUWVlUJIs2HotcVfn52/jBMAKRt/Qtvnu7m/jy9mcPk7E6pfXeDU18dGsaKfFloglCLx99x9SiYlW2MSLwqb4d69h51jQTs6aRQGzhSZU3FZg8go2dF5/ZG2YbI8bxSeDOlM6q2/i9aEwaSJtnJenJCn1T7Gbs7uLWvGKdTBmfnA4fSteXeXwfV+aNl6bhLbWLlyPPVftELgTex2slfq3Vt3IkeCLyfEjSkIHY08rCmZxs+OlT5Po27E12rlcDranq89iKzWX2j+LwBXojbdXroMBiTGhAorCZ3B+5vcyvjETRTPUEVkmOugsG+L+QmdxHyzlsP82MwHL8kqPricjrLdxY4t2RyShtG6Dd3F425V0zTaUd62m9PklfFkkORdMwIdISOB0rl9iBLZGNJf5K9+9h7Hk2uAQjc8nzp/W0TiIs4EIj7Tcxti3DTGTPGRYuaMDMYCWCubgUZoaEEZo3M2SMUHfNfH+au7PMFL4QGwxu4c/j2btZ+ziWZfUdUiNSZaBpFvmsxMNZ9wdDakSqLLx4ZD4/wyODeQkyqPQwtpPVzd7UDzPMMMMMPf4BTrogPAcmKlcAAAAASUVORK5CYII='
ExitImage = b'iVBORw0KGgoAAAANSUhEUgAAADIAAAAyCAYAAAAeP4ixAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAEkUlEQVR4Xr2az08TQRTHF0TS8rOoiQcvRq96QKPhpsYD/4ExMQjbtBAxEAjBiweVg4nhoCeVGIMJB00sbSEQCPKrUAoXT578CzCgiAkY+aHP93botoXdzuzMtE02admZN+8z35k382YwDM4Henr6YXz8Oq9cId9De3tQ2j7s7ZWggUEwDIDKSoCxsUZpYwoVoaLih+VDOHzHsxnY3T0OodCAZSD9VFTsQCzm3Zjn1lkFbKsK/P7vOT6Y5lNhcwhRhhBvcwykYfz+bRgZCQsbkyyIbZxEiA1HH0KhV1yzCFECpjnkaCADswXDww+4xiQLoBLnXSHSPpjmYF7zqEQsL0TakM+3jQ12SfrqWg2VuIwQm0I+hEJPHA2hEhNCBjLK/IZIpFcXDESjTTixdz35YJq57UNr62tPBjLKAMTjD1VhYHS0D5XIBJbsIMP7Hg53sujQ3d0rBZENE4m8kIVBJSalIZgP/6Cz8waDqatbV4Kh3ozHB7zC4Jz4qggBEAh8y2kX/6AG4/MBzpmoKAwGiw3tEJYqyeRZhMldgHjj8/B7UiYW+8yDQSVAA8Qv9/CXSl1BGLYlkH1ImeFhrO78QVB1iNraXex4f/61JJlsRJgtaRDqAIIhhwEupRvD7xe0KFFbC7CwUM9TnU3+VKoJA8COEgwNs0iEYBrwqcfoBLhOyCtNHRQIACwt3RKCsHtwcfGRVVF2iKWViccB1wkdwwkgkXjsCcKGWV5+rgxTXg5Aj0qH0HBKpd5JQWQpE8VhpuaIKkQisaEEYcOkUkPKysjAsDnhGgGl4GBx8X1RlSGIhQW9EFnKvCmKMgSRTBYGwoZJJj8VFIatE4WFyFLmS0GGWSHmBG8iofSrWpUhiESCFtAyXtva38PKCkBVlXpopuMmjE74yb9/ykNQKkuHjZYaa2uGsbcnayJTb3/fMNbX6be0P9JOWHsn2fTUaU1h+UxxJrk92SmfUN0AOsGwfKY4MFryiXyrPCefkR5C2RW15BMiW5WDfEaL04eNFFwJp7Q5EtnUClM0JQ7DkDLxeJ8WGO3RSWRoZZdhmeZdJRgtmZ2OxIopc1sKRosS7IIIYGJCfQfA1plWTzDWnFBdJ2jrQgAA5/A5BVNTANXVatsZts6EhGC0RCdyeGbGOkGxF1GAqzA3B1BTowbD1pn7eWFQiTnlbQc5Oj1NEKePhHCAEzA7qwcmGnW+IKX7QWUISopwK86TnhInoLJeI1h2eTZn7h1pSwvE/DwXwh5qBKPj3CwWu2nD4MReVeodyRwbz6pAOdNk60yJBYMQf6RBBIeT23DD0xl1Zdra2OUoXsafQZC/nmHYCaDwcHKFWV6WhwkGc9vHy9AuTyAHOTZvYou+t5TxeqLZ3OzciXg9/VEIhpTQfQJII4PmjGgAQCXw/wKOuXYUKjOZF4adOw2J9rTXcng685ML09JCEPzTFlTmgyMMi05qO1EBMlTmmSsMU4IPYcd503yZA8POYq8J+KGlCHZYwxEYtznBaxGjWb8Fw04AL/LKF+K9HQCCwVkl+3gZ34tKBJSMKFaGjg7ucP4Pc7yAommR+nUAAAAASUVORK5CYII='
glutenFreeImage = b'iVBORw0KGgoAAAANSUhEUgAAAEAAAAA+CAYAAACbQR1vAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAA8QSURBVGhD1ZsHjNTFF8cHVNSzoKCnYi8IiqinxtjRE0sUWwwaLMSCSEQsd5jTSBC7op4Se6yAerFExS7YS0CPk1PgREU9z0KxnZWiOP/3edk3zm/Zvd293TX5f5PJ7s5vynvfefPmzcxvu3iBKzMydUFely5dUr+yI58yxeA/I2DZsmXujz/+cAsXLnQLFixwv//+u/v7779VwdVXX92ts846rlevXq6ystJVVFS4VVddtezKg5IRkN4Myn3xxRfuzTffdC+99JKbPXu2Kr906dKgeAzqd+vWza255ppuyy23dLvttps7/PDD3X777afEpKNk5EBAqSCKeVHaX3fddb53795+lVVW8SJoxiQj7FdbbTVNlOvatavmI5KVIU8I8fvuu69/6KGH/A8//OBXrFgRUilQlAXEVT/++GN35ZVXuilTpqi5A3u+0UYbuf79+7uddtrJ9evXz2222WZq6mussYaWYTowLdra2lxzc7NraWlx8+bNc7/88ovWFzK0XI8ePdzZZ5/tLrzwQtezZ099BnjeaUjDncI///yjoyCC+xEjRnhRJowaaauttvIiqH/33Xe9zP28RszaJP3000/+mWee8aeeeqrfYIMNglWQ+D1hwgT/559/qtUVg04TQMePP/64l5EIJoxZDxw40D/77LNerEAVilMuEqxMXJ7P3377zd96662+T58+YarwKdbkZ86cmardORRMAIqLafqTTjopofjuu+/u33rrraJHJBsgAlLvv/9+v8kmm2i/1vfNN9/s//rrr2A9lM0XBRFAw59//rmXuRyUX2+99dQcly9fHkatHDDlSDhDph0OFBmQ5ZRTTglTreQEmGKzZs3yskQFE6yqqvLz588PZcqNuA++y/LqN95442ANTL/29nZ9ZikX8iIA5ZuamoIzojOmgHjvvDopB+iX6dba2uolZggk7LnnnupAS0KANcLazrwz5S+55BLtvFBz6wxMBvp7+eWX1fz5Td+PPPKIf/DBB3XUDz74YJUNGbGEJUuW5CVbhwTQCQ7PGKbxCy64oGyOLh0ogG9hFWA5lJDZz507V62xpqZGfcBNN92k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'
lactoseFreeImage = b'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'
TextFont = ("Noto Sans", 15)
IngredientsFont = ("Noto Sans", 12)
WrapSize = 70
ImgSize = (50, 50)

layout = [
    [sg.OptionMenu(values=('Gluten', 'Lactose', 'Nuts', "Custom Allergens"), k='-KEYWORDS-', default_value='Gluten'),
     sg.Input(key='-CUSWORDS-', do_not_clear=True, visible=False, expand_x=True)],
    [sg.Text("Input Link", text_color='black')],
    [sg.Input(key='-INPUT-', do_not_clear=True, size=(50, 50), focus=True)],
    [sg.Text(key="-PRODUCTNAME-", border_width=0, pad=0, text_color="black"),
     sg.Text(key='-ALLERGENSTATUS-', border_width=0, pad=0),
     sg.Image(key="-CERTIFIEDALLERGENS-", expand_x=True, expand_y=True, subsample=8, visible=False)],
    [sg.Text(key="-INGREDIENTS-", border_width=0, pad=0, font=IngredientsFont, text_color='black'),
     sg.Image(productImageDir, expand_x=True, expand_y=True, key="-PRODUCTIMAGE-", subsample=4)],
    [sg.Text(key="-ALLERGENS-", border_width=0, pad=0, font=IngredientsFont, text_color='red')],
    [sg.Button('', image_data=SubmitImage, image_size=(50, 50), key="-SUBMIT-", border_width=0),
     sg.Button('', image_data=ExitImage, image_size=(50, 50), key="-EXIT-", border_width=0)]]

window = sg.Window("SafeBites", layout, auto_size_buttons=False, default_button_element_size=(12, 1),
                   use_default_focus=False, finalize=False)


def convertTuple(tup):
    # initialize an empty string
    str = ''
    for item in tup:
        str = str + item + ", "
    return str


def randomProduct(company):
    with open('Main/websites.json', 'r') as file:
        data = json.load(file)
    urls = data.get(company, [])
    return random.choice(urls)


def CheckForAllergens(returnedIngredients, name, certified):
    IngredientsToBeChecked = str(returnedIngredients).lower()
    print("checking")
    if certified == "Glutenfree" and values["-KEYWORDS-"] == "Gluten":
        dataSet["Ingredients"] = textwrap3.fill(returnedIngredients, WrapSize)
        dataSet["ProductTitle"] = name
        dataSet["AllergenStatus"] = False
        dataSet["DetectedAllergens"] = "Certified Gluten Free"
        PrintResult()
    if certified == "Lactose Free" and values["-KEYWORDS-"] == "Lactose":
        dataSet["Ingredients"] = textwrap3.fill(returnedIngredients, WrapSize)
        dataSet["ProductTitle"] = name
        dataSet["AllergenStatus"] = False
        dataSet["DetectedAllergens"] = "Certified Lactose Free"
        PrintResult()

    elif re_SelectedKeyWords.search(IngredientsToBeChecked):
        detectedAllergens = re_SelectedKeyWords.findall(IngredientsToBeChecked)
        dataSet["Ingredients"] = textwrap3.fill(returnedIngredients, WrapSize)
        dataSet["ProductTitle"] = name
        dataSet["AllergenStatus"] = True
        dataSet["DetectedAllergens"] = detectedAllergens
        PrintResult()
    else:
        detectedAllergens = re_SelectedKeyWords.findall(IngredientsToBeChecked)
        dataSet["Ingredients"] = textwrap3.fill(returnedIngredients, WrapSize)
        dataSet["ProductTitle"] = name
        dataSet["AllergenStatus"] = False
        dataSet["DetectedAllergens"] = detectedAllergens
        PrintResult()


def PrintResult():
    print(Style.BRIGHT + Fore.BLUE + "Product: " + Fore.YELLOW + dataSet["ProductTitle"] + Style.RESET_ALL)
    window['-PRODUCTIMAGE-'].update(productImageDir, subsample=4)
    if not dataSet["AllergenStatus"]:
        print(Fore.BLUE + "Result: " + Fore.GREEN + values['-KEYWORDS-'] + " Free")
        print(Style.RESET_ALL)
        print("Just to make sure, here are the ingredients: " + dataSet["Ingredients"])
        window['-PRODUCTNAME-'].update(dataSet["ProductTitle"] + " is ")
        window['-ALLERGENSTATUS-'].update((values['-KEYWORDS-'].lower()) + " free!", text_color='green')
        window['-INGREDIENTS-'].update("Ingredients: " + dataSet["Ingredients"])
        if dataSet["DetectedAllergens"] == "Certified Gluten Free":
            window['-CERTIFIEDALLERGENS-'].update(source=glutenFreeImage, visible=True)
            window["-ALLERGENS-"].update("Certified Gluten Free", text_color='green')
        elif dataSet["DetectedAllergens"] == "Certified Lactose Free":
            window['-CERTIFIEDALLERGENS-'].update(source=lactoseFreeImage, visible=True)
            window["-ALLERGENS-"].update("Certified Lactose Free", text_color='green')
        else:
            window["-ALLERGENS-"].update("")
    else:
        print(Fore.BLUE + "Result: " + Fore.RED + "Not " + (values['-KEYWORDS-'].lower()) + " Free")
        print(Style.RESET_ALL)
        print("Here are the ingredients: " + dataSet["Ingredients"])
        print(
            "Here are the marked, potentially " + (values['-KEYWORDS-'].lower()) + " containing ingredients: " +
            Fore.RED + convertTuple(re_SelectedKeyWords.findall(dataSet["Ingredients"])) +
            Style.RESET_ALL)
        window['-PRODUCTNAME-'].update(dataSet["ProductTitle"] + " is ")
        window['-ALLERGENSTATUS-'].update("not " + (values['-KEYWORDS-'].lower()) + " free", text_color='DarkRed')
        window['-INGREDIENTS-'].update("Ingredients: " + dataSet["Ingredients"])
        window['-ALLERGENS-'].update("Allergens: " + convertTuple(dataSet["DetectedAllergens"]), text_color="DarkRed")


while True:
    event, values = window.read(timeout=100)
    InputURL = values["-INPUT-"]
    if values["-KEYWORDS-"] == "Custom Allergens":
        window["-CUSWORDS-"].update(visible=True)
    else:
        window["-CUSWORDS-"].update(visible=False)
    if event == sg.WINDOW_CLOSED or event == "-EXIT-":
        im = Image.open('placeholder.png')
        im.save("ProductImage.png", "png")
        break
    if event == "-SUBMIT-":
        window['-PRODUCTNAME-'].update("Searching...")
        if values["-KEYWORDS-"] == "Gluten":
            re_SelectedKeyWords = re.compile("|".join(GlutenFreeKeyWords))
            AllergenFree = False
            print("Gluten selected")
        elif values["-KEYWORDS-"] == "Lactose":
            re_SelectedKeyWords = re.compile("|".join(LactoseKeyWords))
            AllergenFree = False
            print("Lactose selected")
        elif values["-KEYWORDS-"] == "Nuts":
            re_SelectedKeyWords = re.compile("|".join(DeezNutsKeyWords))
            AllergenFree = False
            print("Nuts selected")
        elif values["-KEYWORDS-"] == "Custom Allergens":
            customAllergens = values["-CUSWORDS-"].split(',')
            customAllergens = [x.strip(' ') for x in customAllergens]
            customAllergens = [x.lower() for x in customAllergens]
            re_SelectedKeyWords = re.compile("|".join(customAllergens))
            print(re_SelectedKeyWords)
        if "ica.se" in InputURL:
            ingredients, name, certified = SearchICA(InputURL)
            CheckForAllergens(ingredients, name, certified)
            print(dataSet)
            print("ICA selected")
        if "coop.se" in InputURL:

            ingredients, name = SearchCOOP(InputURL)
            CheckForAllergens(ingredients, name)
            print(dataSet)
            print("Coop selected")

        if InputURL == "":
            InputURL = randomProduct("ICA")
            print("No input")
            ingredients, name, certified = SearchICA(InputURL)
            CheckForAllergens(ingredients, name, certified)
            print(dataSet)
