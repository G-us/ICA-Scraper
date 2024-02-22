from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import element_to_be_clickable, visibility_of_element_located
from selenium.webdriver.support.wait import WebDriverWait

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


def SearchCOOP(InputURL):
    driver = webdriver.Chrome(options=chrome_options)
    url = InputURL
    print("COOP searching at url: " + url)
    driver.get(url)
    driver.delete_all_cookies()
    # Finding Elements
    WebDriverWait(driver,
                  10).until(element_to_be_clickable((By.ID, "cmpbntyestxt")))
    CookiesBtn = driver.find_element(By.ID, "cmpbntyestxt")
    CookiesBtn.click()
    WebDriverWait(driver, 10).until(
        element_to_be_clickable(
            (By.XPATH, "//*[contains(text(), 'Produktfakta')]")))
    Product_Button = driver.find_element(
        By.XPATH, "//*[contains(text(), 'Produktfakta')]")
    Product_Button.click()
    WebDriverWait(driver, 10).until(visibility_of_element_located((By.ID, "Produktfakta")))
    Product_Ingredients = driver.find_element(
        By.XPATH, "//*[@id='Produktfakta']/div/div[1]/div").text
    Product_Name = driver.find_element(By.CLASS_NAME, "ItemInfo-heading").text
    print(Product_Ingredients)
    print(Product_Name)

    return Product_Ingredients, Product_Name
