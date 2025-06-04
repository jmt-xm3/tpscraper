from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import os

def get_item_pictures(url):
    browser =  webdriver.Chrome()
    browser.get(url)
    # Wait for initial content to load
    WebDriverWait(browser, 15).until(
        EC.presence_of_element_located((By.XPATH, "//div[starts-with(@id, 'pic')]"))
    )
    
    
    scroll_attempts = 0
    found = False
    
    while scroll_attempts < 5 and not found:
        # Scrolling down to find first paint
        target_elements = browser.find_elements(By.ID, "pic1")
        if target_elements:
            found = True
            print(f"Found target element: pic1")
            break
        browser.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)
        scroll_attempts += 1
        time.sleep(1)  # Allow time for new content to load
    
    if not found:
        print(f"Could not find pic after 5 scrolls.")
        browser.quit()
    else:
        pictures = browser.find_elements(By.XPATH, "//div[starts-with(@id, 'pic') and substring(@id, string-length(@id), 1) >= '0' and substring(@id, string-length(@id), 1) <= '9']")
        count = 0
        pictures_list = []
        for pic in pictures:
            name = "pic"+str(count)+".jpg"
            count += 1
            asset = pic.find_element(By.XPATH, ".//img[contains(@class, 'w-100 db lh-solid')]") 
            src = asset.get_attribute('src')
            pictures_list.append({"name":name,"src":src})
    browser.quit()
    print(pictures_list)

get_item_pictures("https://www.tradingpaints.com/showroom/view/923791/Ferrari-296-GT3--SF25")