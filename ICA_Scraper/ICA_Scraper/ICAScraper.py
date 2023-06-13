from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import element_to_be_clickable, visibility_of_element_located
from selenium.webdriver.support.wait import WebDriverWait

from PIL import Image

chrome_options = Options()

chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--headless=new")


def ResizeImage(image, size):
    with Image.open(image) as im:
        im.thumbnail(size)
        im.save(image)
        print("Resized image, name: " + image)
        return image


def convertTuple(tup):
    # initialize an empty string
    str = ''
    for item in tup:
        str = str + item + ", "
    return str


Product_Ingredients = ""
Product_Name = ""

dataSet = {
    "AllergenStatus": False,
    "Ingredients": "",
    "DetectedAllergens": "",
    "ProductTitle": ""
}


def SearchICA(InputURL):
    driver = webdriver.Chrome(options=chrome_options)
    print("ICA Searching at url: " + InputURL)
    driver.get(InputURL)
    driver.delete_all_cookies()
    WebDriverWait(driver, 10).until(
        element_to_be_clickable((By.ID, "onetrust-accept-btn-handler")))
    CookiesBtn = driver.find_element(By.ID, "onetrust-accept-btn-handler")
    CookiesBtn.click()

    WebDriverWait(driver, 10).until(
        visibility_of_element_located(
            (By.XPATH, "//*[contains(text(), 'Ingredienser')]")))
    productName = driver.find_element(
        By.XPATH,
        "/html/body/div[1]/div/div[1]/div[2]/main/div/div[1]/div/div[2]/div/div[1]/h1"
    ).text

    ingredients = driver.find_element(
        By.XPATH,
        "//*[contains(text(), 'Ingredienser')]/following-sibling::*").text
    print(ingredients)
    ingredients = str(ingredients).lower()

    return ingredients, productName
