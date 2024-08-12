from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from urllib.request import urlretrieve
from selenium.common.exceptions import NoSuchElementException as e
import time

from PIL import Image

chrome_options = Options()

chrome_options.add_argument("--no-sandbox")

chrome_options.experimental_options['prefs'] = {
    'profile.managed_default_content_settings.javascript': 2,
    'profile.managed_default_content_settings.images': 2
}


chrome_options.add_argument("--headless=new")


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
    productCertified = ""
    searchingTimerStart = time.perf_counter()
    driver = webdriver.Chrome(options=chrome_options)
    print("ICA Searching at url: " + InputURL)
    driver.get(InputURL)
    #driver.delete_all_cookies()
    #WebDriverWait(driver, 10).until(
       # element_to_be_clickable((By.ID, "onetrust-accept-btn-handler")))
    #CookiesBtn = driver.find_element(By.ID, "onetrust-accept-btn-handler")
    #CookiesBtn.click()

    #WebDriverWait(driver, 10).until(
        #visibility_of_element_located(
           # (By.XPATH, "//*[contains(text(), 'Ingredienser')]")))
    productName = driver.find_element(
        By.CSS_SELECTOR,
        "._display_1e1p0_1"
    ).text
    try:
        driver.find_element(By.XPATH, "//span[contains(.,'Glutenfritt')]")
        productCertified = productCertified + "Glutenfree"
        print("Product is Certified Glutenfree")
    except e:
        productCertified = productCertified + "Not Certified"
        print("Error: Product is not Certified Glutenfree")
    try:
        driver.find_element(By.XPATH, "//span[contains(.,'Laktosfritt')]")
        productCertified = productCertified + "Lactose Free"
        print("Product is Certified Lactose Free")
    except e:
        productCertified = productCertified + "Not Certified"
        print("Error: Product is not Certified Lactose Free")
    ingredients = driver.find_element(
        By.XPATH,
        "//*[contains(text(), 'Ingredienser')]/following-sibling::*").text
    ingredients = ingredients.split("Näringsvärde")[0]

    try:
        allergensInfo = driver.find_element(By.XPATH, "//*[contains(text(), 'Allergener')]/following-sibling::*").text
    except:
        allergensInfo = ""
    else:
        if allergensInfo == "":
            print("No Allergens found")
        else:
            ingredients = ingredients + "\n \n There are listed allergens, here they are: " + allergensInfo

    img_url_element = driver.find_element(By.XPATH,
                                          '/html/body/div[1]/div/div[1]/div[2]/main/div/div[2]/div/ul/li/button/img')
    img_url = img_url_element.get_attribute("src")
    print("Getting image")
    urlretrieve(img_url, "productImage.webp")
    print("Retrived image")

    # Open the WebP image
    print("Convert image to PNG")
    im = Image.open('productImage.webp').convert("RGB")
    im.save("ProductImage.png", "png")
    print("Image converted")
    print(productCertified)
    searchingTimerEnd = time.perf_counter()
    print(f"ICA Scraper took {searchingTimerEnd - searchingTimerStart:0.4f} seconds")

    return ingredients, productName, productCertified
