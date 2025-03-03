import time

from selenium import webdriver

driver = webdriver.Chrome()

driver.maximize_window()
driver.get("https://fedrevdev.cosmicnet.xyz/tpa")
time.sleep(2)

driver.quit()
