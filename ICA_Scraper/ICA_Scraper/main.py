#!/usr/bin/env python
import sys
import PySimpleGUI as sg
from CoopScraper import getIngredients
import re

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
re_SelectedKeyWords = []

SubmitImage = b'iVBORw0KGgoAAAANSUhEUgAAADIAAAAyCAYAAAAeP4ixAAAACXBIWXMAAAsTAAALEwEAmpwYAAAEN0lEQVRoge3YW4hVVRzH8c+a8VKaWg6Wgr2UURIS6tGJSEYjMiuDXgyjnrq+SChIZUgRdIHAqAyiG0UvaU9lkBdQCy+lM2NjPkZaLyppalpoOmf1sM9pduPsc87ex4EJ5vu0zjpr/X/7t9dl/9dimGGGGeb/RGg2wA7GXU5HpD0wLdIWacEpHAp0ldk6lyPNP242hY10Mgsr8ADG1Gl+IbK9hTdn81VRzVrkNrKTq0ezJrC08ubzELEr8tQcDuTVrkUuI13Mi6zDlH5/HY9sD/QEjpTpDUwMTI904Lq0VuRsYFmJD5q3kNCwkb3cj3WBy1LV3ZFXDrJhCX9n9e2kPbIyJNOwOooRL5Z4qdCT96MhI13MK7O5aqLyRp+ZzdpAuVGxLu6IfIxrK1URT5d4O++D96eukW4mlenRN51ORu6bw84igj9yzTm+xsxK1fleOtrZXSRelbqLtcwb+kycxeKiJmAGR3EXfqpUjWzlw05GFo1JHSOdzAosTVU9W2JHM4JQ4lhkib51NR2PNhOz3oisqG6xkR9+Zm0zYmnmsC/wTqpq+Qv5t/N/yVwjB7jibDINxlQaPjib9UWFBqIzmbIHMRqxzO1z2VUkVuYbOMd8fSZOHOWLIgK1KHE4srnyM7SwqGisTCO9tFfLZb69h3NFRepQNSKmNPOSaSQwLVXuKSpQj8j+gTTzUstIW7VcTtbKoBD/mxVPVDCRzTSSTggDvUWCN0JvKjOItMSCcWptd6dSjdpqtGuKUanYgT9CkrbkptbUOlQtl5MP1mBxU6p8sGiQWka6Uz874iU4TWawIFXuzmxVh1prZGusrI3A1H3MKyqSxSbGhuR4oKKzpWisTCMlDge+qWqUWVlUJIs2HotcVfn52/jBMAKRt/Qtvnu7m/jy9mcPk7E6pfXeDU18dGsaKfFloglCLx99x9SiYlW2MSLwqb4d69h51jQTs6aRQGzhSZU3FZg8go2dF5/ZG2YbI8bxSeDOlM6q2/i9aEwaSJtnJenJCn1T7Gbs7uLWvGKdTBmfnA4fSteXeXwfV+aNl6bhLbWLlyPPVftELgTex2slfq3Vt3IkeCLyfEjSkIHY08rCmZxs+OlT5Po27E12rlcDranq89iKzWX2j+LwBXojbdXroMBiTGhAorCZ3B+5vcyvjETRTPUEVkmOugsG+L+QmdxHyzlsP82MwHL8kqPricjrLdxY4t2RyShtG6Dd3F425V0zTaUd62m9PklfFkkORdMwIdISOB0rl9iBLZGNJf5K9+9h7Hk2uAQjc8nzp/W0TiIs4EIj7Tcxti3DTGTPGRYuaMDMYCWCubgUZoaEEZo3M2SMUHfNfH+au7PMFL4QGwxu4c/j2btZ+ziWZfUdUiNSZaBpFvmsxMNZ9wdDakSqLLx4ZD4/wyODeQkyqPQwtpPVzd7UDzPMMMMMPf4BTrogPAcmKlcAAAAASUVORK5CYII='
ExitImage = b'iVBORw0KGgoAAAANSUhEUgAAADIAAAAyCAYAAAAeP4ixAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAEkUlEQVR4Xr2az08TQRTHF0TS8rOoiQcvRq96QKPhpsYD/4ExMQjbtBAxEAjBiweVg4nhoCeVGIMJB00sbSEQCPKrUAoXT578CzCgiAkY+aHP93botoXdzuzMtE02admZN+8z35k382YwDM4Henr6YXz8Oq9cId9De3tQ2j7s7ZWggUEwDIDKSoCxsUZpYwoVoaLih+VDOHzHsxnY3T0OodCAZSD9VFTsQCzm3Zjn1lkFbKsK/P7vOT6Y5lNhcwhRhhBvcwykYfz+bRgZCQsbkyyIbZxEiA1HH0KhV1yzCFECpjnkaCADswXDww+4xiQLoBLnXSHSPpjmYF7zqEQsL0TakM+3jQ12SfrqWg2VuIwQm0I+hEJPHA2hEhNCBjLK/IZIpFcXDESjTTixdz35YJq57UNr62tPBjLKAMTjD1VhYHS0D5XIBJbsIMP7Hg53sujQ3d0rBZENE4m8kIVBJSalIZgP/6Cz8waDqatbV4Kh3ozHB7zC4Jz4qggBEAh8y2kX/6AG4/MBzpmoKAwGiw3tEJYqyeRZhMldgHjj8/B7UiYW+8yDQSVAA8Qv9/CXSl1BGLYlkH1ImeFhrO78QVB1iNraXex4f/61JJlsRJgtaRDqAIIhhwEupRvD7xe0KFFbC7CwUM9TnU3+VKoJA8COEgwNs0iEYBrwqcfoBLhOyCtNHRQIACwt3RKCsHtwcfGRVVF2iKWViccB1wkdwwkgkXjsCcKGWV5+rgxTXg5Aj0qH0HBKpd5JQWQpE8VhpuaIKkQisaEEYcOkUkPKysjAsDnhGgGl4GBx8X1RlSGIhQW9EFnKvCmKMgSRTBYGwoZJJj8VFIatE4WFyFLmS0GGWSHmBG8iofSrWpUhiESCFtAyXtva38PKCkBVlXpopuMmjE74yb9/ykNQKkuHjZYaa2uGsbcnayJTb3/fMNbX6be0P9JOWHsn2fTUaU1h+UxxJrk92SmfUN0AOsGwfKY4MFryiXyrPCefkR5C2RW15BMiW5WDfEaL04eNFFwJp7Q5EtnUClM0JQ7DkDLxeJ8WGO3RSWRoZZdhmeZdJRgtmZ2OxIopc1sKRosS7IIIYGJCfQfA1plWTzDWnFBdJ2jrQgAA5/A5BVNTANXVatsZts6EhGC0RCdyeGbGOkGxF1GAqzA3B1BTowbD1pn7eWFQiTnlbQc5Oj1NEKePhHCAEzA7qwcmGnW+IKX7QWUISopwK86TnhInoLJeI1h2eTZn7h1pSwvE/DwXwh5qBKPj3CwWu2nD4MReVeodyRwbz6pAOdNk60yJBYMQf6RBBIeT23DD0xl1Zdra2OUoXsafQZC/nmHYCaDwcHKFWV6WhwkGc9vHy9AuTyAHOTZvYou+t5TxeqLZ3OzciXg9/VEIhpTQfQJII4PmjGgAQCXw/wKOuXYUKjOZF4adOw2J9rTXcng685ML09JCEPzTFlTmgyMMi05qO1EBMlTmmSsMU4IPYcd503yZA8POYq8J+KGlCHZYwxEYtznBaxGjWb8Fw04AL/LKF+K9HQCCwVkl+3gZ34tKBJSMKFaGjg7ucP4Pc7yAommR+nUAAAAASUVORK5CYII='

TextFont = ("Noto Sans", 15)
IngredientsFont = ("Noto Sans", 12)
WrapSize = 70
ImgSize = (50, 50)

layout = [[sg.OptionMenu(values=('Gluten', 'Lactose', 'Nuts'), k='-KEYWORDS-', default_value='Gluten')],
          [sg.Text("Input Link", text_color='black')],
          [sg.Input(key='-INPUT-', do_not_clear=True)],
          [sg.Text(key="-PRODUCTNAME-", border_width=0, pad=0, text_color="black"),
           sg.Text(key='-ALLERGENSTATUS-', border_width=0, pad=0)],
          [sg.Text(key="-INGREDIENTS-", border_width=0, pad=0, font=IngredientsFont, text_color='black'),
           sg.Image(key="-IMAGE-", pad=0)],
          [sg.Text(key="-ALLERGENS-", border_width=0, pad=0, font=IngredientsFont, text_color='red')],
          [sg.Button('', image_data=SubmitImage, image_size=(50, 50), key="-SUBMIT-", border_width=0),
           sg.Button('', image_data=ExitImage, image_size=(50, 50), key="-EXIT-", border_width=0)]]

window = sg.Window("Select Website", layout, auto_size_buttons=False, default_button_element_size=(12, 1),
                   use_default_focus=False, finalize=True)


def CheckForAllergens(ingredients, name):
    ingredients = str(ingredients).lower()
    print("checking")

    if re_SelectedKeyWords.search(ingredients):
        detectedAllergens = re_SelectedKeyWords.findall(ingredients)
        dataSet["Ingredients"] = ingredients
        dataSet["ProductTitle"] = name
        dataSet["AllergenStatus"] = True
        dataSet["DetectedAllergens"] = detectedAllergens
    else:
        detectedAllergens = re_SelectedKeyWords.findall(ingredients)
        dataSet["Ingredients"] = ingredients
        dataSet["ProductTitle"] = name
        dataSet["AllergenStatus"] = False
        dataSet["DetectedAllergens"] = detectedAllergens


while True:
    event, values = window.read(timeout=100)
    InputURL = values["-INPUT-"]
    if event == sg.WINDOW_CLOSED or event == "-EXIT-":
        break
    if event == "-SUBMIT-":
        if "ica.se" in InputURL:
            print("ICA selected")
            window.close()
        if "coop.se" in InputURL:
            ingredients, name = getIngredients(InputURL)
            CheckForAllergens(ingredients, name)
            print(dataSet)
            print("Coop selected")
            window.close()
        if values["-KEYWORDS-"] == "Gluten":
            re_SelectedKeyWords = re.compile("|".join(GlutenFreeKeyWords))
            AllergenFree = False
        elif values["-KEYWORDS-"] == "Lactose":
            re_SelectedKeyWords = re.compile("|".join(LactoseKeyWords))
            AllergenFree = False
        elif values["-KEYWORDS-"] == "Deez Nuts":
            re_SelectedKeyWords = re.compile("|".join(DeezNutsKeyWords))
        if InputURL == "":
            InputURL = "https://www.coop.se/handla/varor/mejeri-agg/yoghurt-fil/smaksatt-yoghurt/yoghurt-vanilj-passionsfrukt-6408432203411"
            print("No input")
            ingredients, name = getIngredients(InputURL)
            CheckForAllergens(ingredients, name)
            print(dataSet)
