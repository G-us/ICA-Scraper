from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

url = "https://www.coop.se/handla/varor/skafferi/pasta-pastasas/formpasta/pasta-farfalle-8076808060654"

print("Starting search at url: " + url)

driver = webdriver.Chrome(options=chrome_options)
driver.get(url)

## Finding Elements

CookiesBtn = driver.find_element(By.ID, "cmpbntyestxt")

CookiesBtn.click()

Product_Button = driver.find_element(By.XPATH, "/html/body/main/div/div/div/div[2]/div/div/div[2]/div[1]/article/div/div[2]/div[3]/div/div[2]/div/div[1]/button")

Product_Button.click()


Product_Ingredients = driver.find_element(By.XPATH, "/html/body/main/div/div/div/div[2]/div/div/div[2]/div[1]/article/div/div[2]/div[3]/div/div[2]/div/div[2]/div/div/div/div[1]/div").text

print(Product_Ingredients)