import random

import PySimpleGUI as sg
from CoopScraper import SearchCOOP
from ICAScraper import SearchICA
import textwrap3
from ctypes import windll
from PIL import Image
import json
import images

# Enable High DPI Awareness (Windows specific)
windll.shcore.SetProcessDpiAwareness(1)

# Set the PySimpleGUI theme to a light blue color palette
sg.theme('LightBlue3')

# Image directories
productImageDir = r"C:\Users\HenryParsons\PycharmProjects\SafeBites\productImage.png"

# Variables to store previous URL and data
previousURL = ""

dataSet = {
    "AllergenStatus": False,
    "Ingredients": "",
    "DetectedAllergens": "",
    "ProductTitle": "",
    "ProductCertified": "",
    "PotentialAllergens": ""
}

# Keyword lists for allergens
GlutenFreeKeyWords = [
    "vete", "råg", "korn", "kamut", "dinkel", "vetekli", "kruskakli", "spelt", "durum", "havregryn",
    "mannagryn"
]

GlutenKeyWords = ["glutenfri", "glutenfritt", "glutenfria", "gluten free"]

LactoseKeyWords = [
    "mjölk", "mjölkprotein", "mjölkproteinhydrolysat", "mjölkproteinisolat", "mjölkproteinkoncentrat", "laktose",
    "grädde", "smör", "ost"
]

LactoseFreeKeyWords = ["Laktosfri", "Laktosfritt", "Laktosfria"]

DeezNutsKeyWords = ["nöt", "jordnöt", "mandel", "cashewnöt", "hasselnöt", "valnöt", "pistagenöt", "pecannöt",
                    "macadamianöt", "paranöt", "kastanjenöt"]

customKeyWords = []
PosSelectedKeyWords = []
NegSelectedKeyWords = []

# Image files (Ensure these images are in the same directory or provide correct paths)
SubmitImage = images.SubmitImage
ExitImage = images.ExitImage
glutenFreeImage = images.glutenFreeImage
lactoseFreeImage = images.lactoseFreeImage
loadingGif = "kOnzy.gif"

# Font settings
TitleFont = ("Helvetica", 16, 'bold')
TextFont = ("Helvetica", 12)
IngredientsFont = ("Helvetica", 10)
WrapSize = 80
ImgSize = (200, 200)

# Layout of the GUI
layout = [
    [sg.Text("SafeBites - Allergen Checker", font=TitleFont, justification='center', expand_x=True)],
    [sg.Frame('Select Allergen', [[
        sg.Combo(values=('Gluten', 'Lactose', 'Nuts', "Custom Allergens"), key='-KEYWORDS-', default_value='Gluten', font=TextFont, readonly=True),
        sg.InputText(key='-CUSWORDS-', do_not_clear=True, visible=False, expand_x=True, font=TextFont, size=(30, 1), disabled_readonly_background_color='LightBlue3')
    ]], relief='flat', expand_x=True)],
    [sg.Text("Input Product Link:", font=TextFont)],
    [sg.InputText(key='-INPUT-', do_not_clear=True, size=(50, 1), focus=True, font=TextFont, expand_x=True)],
    [sg.HorizontalSeparator()],
    [sg.Text(key="-PRODUCTNAME-", font=("Helvetica", 14, 'bold'), text_color="DarkBlue")],
    [sg.Text(key='-ALLERGENSTATUS-', font=("Helvetica", 12), text_color="black")],
    [sg.Image(key="-CERTIFIEDALLERGENS-", visible=False)],
    [sg.Image(productImageDir, key="-PRODUCTIMAGE-", size=ImgSize, subsample=2)],
    [sg.Text(key="-INGREDIENTS-", font=IngredientsFont, text_color='black', size=(80, None))],
    [sg.Text(key="-ALLERGENS-", font=IngredientsFont, text_color='red', size=(80, None))],
    [sg.Text(key="-POTALLERGENS-", font=IngredientsFont, text_color='darkgoldenrod', size=(80, None))],
    [sg.HorizontalSeparator()],
    [sg.Button('Submit', key="-SUBMIT-", size=(10, 1), font=TextFont),
     sg.Button('Exit', key="-EXIT-", size=(10, 1), font=TextFont)]
]

# Create the window
window = sg.Window("SafeBites - Allergen Checker", layout, finalize=True, element_justification='center')

def convertTuple(tup):
    """Converts a tuple to a string."""
    return ', '.join(tup)

def randomProduct(company):
    with open('Main/websites.json', 'r') as file:
        data = json.load(file)
    urls = data.get(company, [])
    return random.choice(urls)

def containsAllergens(ingredient, positiveWords, negativeWords):
    if any(negativeWord in ingredient.lower() for negativeWord in negativeWords):
        return False
    if any(positiveWord in ingredient.lower() for positiveWord in positiveWords):
        return True
    return False

def check_ingredients(ingredients_list, positiveWords, negativeWords):
    ingredients = ingredients_list.split(',')
    flagged_ingredients = [ingredient.strip() for ingredient in ingredients if containsAllergens(ingredient, positiveWords, negativeWords)]
    return flagged_ingredients

def AllergenCheckingPt1(ingredients, positiveWords, negativeWords):
    flagged_ingredients = check_ingredients(ingredients, positiveWords, negativeWords)
    if flagged_ingredients:
        dataSet["AllergenStatus"] = True
        dataSet["DetectedAllergens"] = flagged_ingredients
        AllergenCheckingPt2()
    else:
        dataSet["AllergenStatus"] = False
        AllergenCheckingPt2()

def AllergenCheckingPt2():
    if dataSet["ProductCertified"].__contains__("Glutenfree") and values["-KEYWORDS-"] == "Gluten":
        dataSet["AllergenStatus"] = False
        dataSet["DetectedAllergens"] = "Certified Gluten Free"
        PrintResult()
    elif dataSet["ProductCertified"].__contains__("Lactose Free") and values["-KEYWORDS-"] == "Lactose":
        dataSet["AllergenStatus"] = False
        dataSet["DetectedAllergens"] = "Certified Lactose Free"
        PrintResult()
    elif dataSet["AllergenStatus"]:
        dataSet["AllergenStatus"] = True
        PrintResult()
    else:
        dataSet["AllergenStatus"] = False
        PrintResult()

def PrintResult():
    window.refresh()
    window['-PRODUCTIMAGE-'].update(productImageDir, subsample=4)
    if not dataSet["AllergenStatus"]:
        window['-PRODUCTNAME-'].update(dataSet["ProductTitle"], text_color='DarkBlue')
        window['-ALLERGENSTATUS-'].update((values['-KEYWORDS-'].lower()) + " free!", text_color='green')
        window['-INGREDIENTS-'].update("Ingredients: " + dataSet["Ingredients"])
        if dataSet["PotentialAllergens"]:
            window['-POTALLERGENS-'].update(
                textwrap3.fill("Listed Allergens: " + dataSet["PotentialAllergens"], WrapSize),
                text_color="DarkGoldenrod")
        else:
            window['-POTALLERGENS-'].update("")
        if dataSet["DetectedAllergens"] == "Certified Gluten Free":
            window['-CERTIFIEDALLERGENS-'].update(filename=glutenFreeImage, visible=True)
            window["-ALLERGENS-"].update("Certified Gluten Free", text_color='green')
        elif dataSet["DetectedAllergens"] == "Certified Lactose Free":
            window['-CERTIFIEDALLERGENS-'].update(filename=lactoseFreeImage, visible=True)
            window["-ALLERGENS-"].update("Certified Lactose Free", text_color='green')
        else:
            window["-ALLERGENS-"].update("")
    else:
        window['-PRODUCTNAME-'].update(dataSet["ProductTitle"], text_color='DarkBlue')
        window['-ALLERGENSTATUS-'].update("Not " + (values['-KEYWORDS-'].lower()) + " free", text_color='DarkRed')
        window['-INGREDIENTS-'].update("Ingredients: " + dataSet["Ingredients"])
        window['-ALLERGENS-'].update(textwrap3.fill("Allergens: " + convertTuple(dataSet["DetectedAllergens"]), WrapSize),
                                     text_color="DarkRed")
        if dataSet["PotentialAllergens"]:
            window['-POTALLERGENS-'].update(textwrap3.fill("Listed Allergens: " + dataSet["PotentialAllergens"], WrapSize),
                                            text_color="DarkGoldenrod")
        else:
            window['-POTALLERGENS-'].update("")

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
        window['-PRODUCTNAME-'].update("Searching...", text_color='DarkBlue')
        window['-PRODUCTIMAGE-'].update_animation(loadingGif, time_between_frames=100)
        window['-CERTIFIEDALLERGENS-'].update(visible=False)
        if values["-KEYWORDS-"] == "Gluten":
            PosSelectedKeyWords = GlutenFreeKeyWords
            NegSelectedKeyWords = GlutenKeyWords
            print("Gluten selected")
            AllergenFree = False
        elif values["-KEYWORDS-"] == "Lactose":
            PosSelectedKeyWords = LactoseKeyWords
            NegSelectedKeyWords = LactoseFreeKeyWords
            print("Lactose selected")
            AllergenFree = False
        elif values["-KEYWORDS-"] == "Nuts":
            PosSelectedKeyWords = DeezNutsKeyWords
            NegSelectedKeyWords = ""
            print("Nuts selected")
            AllergenFree = False
        elif values["-KEYWORDS-"] == "Custom Allergens":
            customAllergens = values["-CUSWORDS-"].split(',')
            customAllergens = [x.strip(' ') for x in customAllergens]
            customAllergens = [x.lower() for x in customAllergens]
            PosSelectedKeyWords = customAllergens
            print("Custom Allergens selected:", PosSelectedKeyWords)
        if "ica.se" in InputURL:
            print("ICA selected")
            if previousURL == InputURL:
                ingredients = dataSet["Ingredients"]
                name = dataSet["ProductTitle"]
                certified = dataSet["ProductCertified"]
                AllergenCheckingPt1(ingredients, PosSelectedKeyWords, NegSelectedKeyWords)
            else:
                ingredients, name, certified = SearchICA(InputURL)
                try:
                    finalIngredients, potentialAllergens = ingredients.split("?")
                except:
                    finalIngredients = ingredients
                    potentialAllergens = ""
                dataSet["PotentialAllergens"] = potentialAllergens
                dataSet["Ingredients"] = textwrap3.fill(finalIngredients, WrapSize)
                dataSet["ProductTitle"] = name
                dataSet["ProductCertified"] = certified
                AllergenCheckingPt1(finalIngredients, PosSelectedKeyWords, NegSelectedKeyWords)
                print(dataSet)
            previousURL = InputURL
        elif "coop.se" in InputURL:
            print("COOP selected")
            if previousURL == InputURL:
                ingredients = dataSet["Ingredients"]
                name = dataSet["ProductTitle"]
                certified = dataSet["ProductCertified"]
                AllergenCheckingPt1(ingredients, PosSelectedKeyWords, NegSelectedKeyWords)
            else:
                ingredients, name, certified = SearchCOOP(InputURL)
                dataSet["Ingredients"] = textwrap3.fill(ingredients, WrapSize)
                dataSet["ProductTitle"] = name
                dataSet["ProductCertified"] = certified
                AllergenCheckingPt1(ingredients, PosSelectedKeyWords, NegSelectedKeyWords)
                print(dataSet)
            previousURL = InputURL
        elif InputURL == "":
            InputURL = randomProduct("ICA")
            print("No input provided, selecting random product")
            ingredients, name, certified = SearchCOOP(InputURL)
            AllergenCheckingPt2()
            print(dataSet)