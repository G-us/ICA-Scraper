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

dataSet = {
  "AllergenStatus": False,
  "Ingredients": "",
  "DetectedAllergens": "",
  "ProductTitle": ""
}

Product_Ingredients = ""
Product_Name = ""

chrome_options = Options()


chrome_options.add_argument("--no-sandbox") 



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
    WebDriverWait(driver, 10).until(element_to_be_clickable((By.CSS_SELECTOR,
                                                             "body > main > div > div > div > div.Grid-cell.Grid-cell--grownWidth > div > div > div.Grid > div.Grid-cell.u-marginBxlg > article > div > div.ItemInfo-details > div:nth-child(3) > div > div:nth-child(2) > div > div.w7Fswr5F > button")))
    Product_Button = driver.find_element(By.CSS_SELECTOR,
                                         "body > main > div > div > div > div.Grid-cell.Grid-cell--grownWidth > div > div > div.Grid > div.Grid-cell.u-marginBxlg > article > div > div.ItemInfo-details > div:nth-child(3) > div > div:nth-child(2) > div > div.w7Fswr5F > button")
    Product_Button.click()
    WebDriverWait(driver, 10).until(visibility_of_element_located((By.ID, "Produktfakta")))
    Product_Ingredients = driver.find_element(By.ID,
                                              "Produktfakta").text
    Product_Name = driver.find_element(By.CLASS_NAME, "ItemInfo-heading").text
    print(Product_Ingredients)
    print(Product_Name)

    return Product_Ingredients, Product_Name

