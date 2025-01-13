import random
import PySimpleGUI as sg
from CoopScraper import SearchCOOP
from ICAScraper import SearchICA
from ctypes import windll
from PIL import Image
import json
import images

# Enable High DPI Awareness (Windows specific)
try:
    windll.shcore.SetProcessDpiAwareness(1)
except:
    pass

# Set the PySimpleGUI theme to a light blue color palette
sg.theme('LightBlue3')

# Image directories (Ensure these paths are correct)
productImageDir = "productImage.png"

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
    "mjölk", "mjölkprotein", "mjölkproteinhydrolysat", "mjölkproteinisolat",
    "mjölkproteinkoncentrat", "laktose", "grädde", "smör", "ost"
]

LactoseFreeKeyWords = ["laktosfri", "laktosfritt", "laktosfria"]

DeezNutsKeyWords = [
    "nöt", "jordnöt", "mandel", "cashewnöt", "hasselnöt", "valnöt",
    "pistagenöt", "pecannöt", "macadamianöt", "paranöt", "kastanjenöt"
]

customKeyWords = []
PosSelectedKeyWords = []
NegSelectedKeyWords = []

# Image files (Ensure these images are in the same directory or provide correct paths)
glutenFreeImage = images.glutenFreeImage
lactoseFreeImage = images.lactoseFreeImage
loadingGif = r"C:\Users\HenryParsons\PycharmProjects\SafeBites\kOnzy.gif"

# Font settings (Reduced sizes for better window fit)
TitleFont = ("Helvetica", 14, 'bold')
TextFont = ("Helvetica", 10)
IngredientsFont = ("Helvetica", 9)
WrapSize = 60
ImgSize = (150, 150)

# Layout of the GUI with adjusted sizes
layout = [
    [sg.Text("SafeBites - Allergen Checker", font=TitleFont, justification='center', expand_x=True)],
    [sg.Frame('Select Allergen', [[
        sg.Combo(values=('Gluten', 'Lactose', 'Nuts', "Custom Allergens"), key='-KEYWORDS-',
                 default_value='Gluten', font=TextFont, readonly=True),
        sg.InputText(key='-CUSWORDS-', do_not_clear=True, visible=False, expand_x=True,
                     font=TextFont, size=(20, 1),
                     disabled_readonly_background_color='LightBlue3')
    ]], relief='flat', expand_x=True)],
    [sg.Text("Input Product Link:", font=TextFont)],
    [sg.InputText(key='-INPUT-', do_not_clear=True, size=(40, 1), focus=True, font=TextFont, expand_x=True)],
    [sg.HorizontalSeparator()],
    [sg.Text(key="-PRODUCTNAME-", font=("Helvetica", 12, 'bold'), text_color="DarkBlue")],
    [sg.Text(key='-ALLERGENSTATUS-', font=("Helvetica", 10), text_color="black")],
    [sg.Image(key="-CERTIFIEDALLERGENS-", visible=False)],
    [sg.Image(productImageDir, key="-PRODUCTIMAGE-", size=ImgSize, subsample=2)],
    [sg.Multiline(key="-INGREDIENTS-", font=IngredientsFont, text_color='black',
                  size=(60, 5), no_scrollbar=True, disabled=False,
                  background_color='LightBlue3')],
    [sg.Text(key="-ALLERGENS-", font=IngredientsFont, text_color='red', size=(60, None))],
    [sg.Text(key="-POTALLERGENS-", font=IngredientsFont, text_color='darkgoldenrod', size=(60, None))],
    [sg.HorizontalSeparator()],
    [sg.Button('Submit', key="-SUBMIT-", size=(8, 1), font=TextFont),
     sg.Button('Exit', key="-EXIT-", size=(8, 1), font=TextFont)]
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
    if "Glutenfree" in dataSet["ProductCertified"] and values["-KEYWORDS-"] == "Gluten":
        dataSet["AllergenStatus"] = False
        dataSet["DetectedAllergens"] = "Certified Gluten Free"
    elif "Lactose Free" in dataSet["ProductCertified"] and values["-KEYWORDS-"] == "Lactose":
        dataSet["AllergenStatus"] = False
        dataSet["DetectedAllergens"] = "Certified Lactose Free"
    PrintResult()

def PrintResult():
    window.refresh()
    window['-PRODUCTIMAGE-'].update(productImageDir, subsample=4)
    if not dataSet["AllergenStatus"]:
        window['-PRODUCTNAME-'].update(dataSet["ProductTitle"], text_color='DarkBlue')
        window['-ALLERGENSTATUS-'].update((values['-KEYWORDS-'].lower()) + " free!", text_color='green')
        highlight_ingredients(dataSet["Ingredients"], PosSelectedKeyWords)
        if dataSet["PotentialAllergens"]:
            window['-POTALLERGENS-'].update(
                "Listed Allergens: " + dataSet["PotentialAllergens"], text_color="DarkGoldenrod")
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
        highlight_ingredients(dataSet["Ingredients"], PosSelectedKeyWords)
        window['-ALLERGENS-'].update("Allergens: " + convertTuple(dataSet["DetectedAllergens"]), text_color="DarkRed")
        if dataSet["PotentialAllergens"]:
            window['-POTALLERGENS-'].update("Listed Allergens: " + dataSet["PotentialAllergens"], text_color="DarkGoldenrod")
        else:
            window['-POTALLERGENS-'].update("")

def highlight_ingredients(ingredients_text, allergens):
    # Clear the Multiline widget
    window['-INGREDIENTS-'].update(value='')

    # Access the underlying tk.Text widget
    ml_widget = window['-INGREDIENTS-'].Widget

    # Enable the widget temporarily to allow updates
    ml_widget.config(state='normal')

    # Remove existing tags
    ml_widget.tag_delete('highlight')

    # Insert the full ingredients text
    ml_widget.insert('1.0', ingredients_text)

    # Configure tag for highlighting
    ml_widget.tag_configure('highlight', foreground='red')

    # Find and highlight allergens in the text
    for allergen in allergens:
        start_pos = '1.0'
        while True:
            idx = ml_widget.search(allergen, start_pos, nocase=1, stopindex='end')
            if not idx:
                break
            end_pos = f"{idx}+{len(allergen)}c"
            ml_widget.tag_add('highlight', idx, end_pos)
            start_pos = end_pos

    # Re-disable the widget to prevent user edits
    ml_widget.config(state='disabled')

while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED or event == "-EXIT-":
        im = Image.open('placeholder.png')
        im.save("ProductImage.png", "png")
        break
    InputURL = values.get("-INPUT-", "")
    if values.get("-KEYWORDS-", "") == "Custom Allergens":
        window["-CUSWORDS-"].update(visible=True)
    else:
        window["-CUSWORDS-"].update(visible=False)
    if event == "-SUBMIT-":
        window['-PRODUCTNAME-'].update("Searching...", text_color='DarkBlue')
        window['-PRODUCTIMAGE-'].update_animation(loadingGif, time_between_frames=100)
        window['-CERTIFIEDALLERGENS-'].update(visible=False)
        window['-ALLERGENS-'].update("")
        window['-INGREDIENTS-'].update("")
        PosSelectedKeyWords = []
        NegSelectedKeyWords = []
        if values["-KEYWORDS-"] == "Gluten":
            PosSelectedKeyWords = GlutenFreeKeyWords
            NegSelectedKeyWords = GlutenKeyWords
        elif values["-KEYWORDS-"] == "Lactose":
            PosSelectedKeyWords = LactoseKeyWords
            NegSelectedKeyWords = LactoseFreeKeyWords
        elif values["-KEYWORDS-"] == "Nuts":
            PosSelectedKeyWords = DeezNutsKeyWords
            NegSelectedKeyWords = []
        elif values["-KEYWORDS-"] == "Custom Allergens":
            customAllergens = values["-CUSWORDS-"].split(',')
            customAllergens = [x.strip().lower() for x in customAllergens]
            PosSelectedKeyWords = customAllergens
            NegSelectedKeyWords = []
        else:
            sg.popup("Please select an allergen.", title="No Allergen Selected")
            continue

        if "ica.se" in InputURL:
            print("ICA selected")
            if previousURL == InputURL:
                ingredients = dataSet["Ingredients"]
                AllergenCheckingPt1(ingredients, PosSelectedKeyWords, NegSelectedKeyWords)
            else:
                ingredients, name, certified = SearchICA(InputURL)
                try:
                    finalIngredients, potentialAllergens = ingredients.split("?")
                except:
                    finalIngredients = ingredients
                    potentialAllergens = ""
                dataSet["PotentialAllergens"] = potentialAllergens
                dataSet["Ingredients"] = finalIngredients
                dataSet["ProductTitle"] = name
                dataSet["ProductCertified"] = certified
                AllergenCheckingPt1(finalIngredients, PosSelectedKeyWords, NegSelectedKeyWords)
                previousURL = InputURL
        elif "coop.se" in InputURL:
            print("COOP selected")
            if previousURL == InputURL:
                ingredients = dataSet["Ingredients"]
                AllergenCheckingPt1(ingredients, PosSelectedKeyWords, NegSelectedKeyWords)
            else:
                ingredients, name, certified = SearchCOOP(InputURL)
                dataSet["Ingredients"] = ingredients
                dataSet["ProductTitle"] = name
                dataSet["ProductCertified"] = certified
                AllergenCheckingPt1(ingredients, PosSelectedKeyWords, NegSelectedKeyWords)
                previousURL = InputURL
        else:
            sg.popup("Please enter a valid ICA or COOP product URL.", title="Invalid URL")
