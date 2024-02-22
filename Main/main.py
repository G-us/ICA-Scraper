#!/usr/bin/env python
import PySimpleGUI as sg
from CoopScraper import SearchCOOP
import re
from ICAScraper import SearchICA
import textwrap3
from colorama import Fore, Style

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
     sg.Text(key='-ALLERGENSTATUS-', border_width=0, pad=0)],
    [sg.Text(key="-INGREDIENTS-", border_width=0, pad=0, font=IngredientsFont, text_color='black'),
     sg.Image(key="-IMAGE-", pad=0)],
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


def CheckForAllergens(returnedIngredients, name):
    returnedIngredients = str(returnedIngredients).lower()
    print("checking")

    if re_SelectedKeyWords.search(returnedIngredients):
        detectedAllergens = re_SelectedKeyWords.findall(returnedIngredients)
        dataSet["Ingredients"] = textwrap3.fill(returnedIngredients, WrapSize)
        dataSet["ProductTitle"] = name
        dataSet["AllergenStatus"] = True
        dataSet["DetectedAllergens"] = detectedAllergens
        PrintResult()
    else:
        detectedAllergens = re_SelectedKeyWords.findall(returnedIngredients)
        dataSet["Ingredients"] = textwrap3.fill(returnedIngredients, WrapSize)
        dataSet["ProductTitle"] = name
        dataSet["AllergenStatus"] = False
        dataSet["DetectedAllergens"] = detectedAllergens
        PrintResult()


def PrintResult():
    print(Style.BRIGHT + Fore.BLUE + "Product: " + Fore.YELLOW + dataSet["ProductTitle"] + Style.RESET_ALL)
    if not dataSet["AllergenStatus"]:
        print(Fore.BLUE + "Result: " + Fore.GREEN + values['-KEYWORDS-'] + " Free")
        print(Style.RESET_ALL)
        print("Just to make sure, here are the ingredients: " + dataSet["Ingredients"])
        window['-PRODUCTNAME-'].update(dataSet["ProductTitle"] + " is ")
        window['-ALLERGENSTATUS-'].update((values['-KEYWORDS-'].lower()) + " free!", text_color='green')
        window['-INGREDIENTS-'].update("Ingredients: " + dataSet["Ingredients"])
        window['-ALLERGENS-'].update("")
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
        window['-ALLERGENS-'].update("Allergens: " + convertTuple(re_SelectedKeyWords.findall(dataSet["Ingredients"])), text_color="DarkRed")


while True:
    event, values = window.read(timeout=100)
    InputURL = values["-INPUT-"]
    if values["-KEYWORDS-"] == "Custom Allergens":
        window["-CUSWORDS-"].update(visible=True)
    else:
        window["-CUSWORDS-"].update(visible=False)
    if event == sg.WINDOW_CLOSED or event == "-EXIT-":
        break
    if event == "-SUBMIT-":
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
            ingredients, name = SearchICA(InputURL)
            CheckForAllergens(ingredients, name)
            print(dataSet)
            print("ICA selected")
        if "coop.se" in InputURL:
            ingredients, name = SearchCOOP(InputURL)
            CheckForAllergens(ingredients, name)
            print(dataSet)
            print("Coop selected")

        if InputURL == "":
            InputURL = "https://www.coop.se/handla/varor/brod-bageri/ostkex-majskakor-tilltugg/majskakor-riskakor/majskakor-graddfil-lok-7340011469773"
            print("No input")
            ingredients, name = SearchCOOP(InputURL)
            CheckForAllergens(ingredients, name)
            print(dataSet)
