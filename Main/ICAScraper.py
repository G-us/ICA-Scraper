from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import element_to_be_clickable, visibility_of_element_located
from selenium.webdriver.support.wait import WebDriverWait
from urllib.request import urlretrieve

from PIL import Image

chrome_options = Options()

chrome_options.add_argument("--no-sandbox")


#chrome_options.add_argument("--headless=new")


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
        By.CSS_SELECTOR,
        "._display_1e1p0_1"
    ).text

    ingredients = driver.find_element(
        By.XPATH,
        "//*[contains(text(), 'Ingredienser')]/following-sibling::*").text
    print(ingredients)
    ingredients = ingredients.split("Näringsvärde")[0]
    img_url_element = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[1]/div[2]/main/div/div[2]/div/ul/li/button/img')
    img_url = img_url_element.get_attribute("src")
    urlretrieve(img_url, "productImage.webp")

    # Open the WebP image
    im = Image.open('productImage.webp').convert("RGB")
    im.save("ProductImage.png", "png")

    return ingredients, productName
