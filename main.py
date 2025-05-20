from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import json
from urllib.request import urlretrieve


def get_all_showroom_paints(profile_url,first_paint_id,maxiumum_scroll_attempts):
    browser = webdriver.Firefox()
    browser.get(profile_url)
    
    # Wait for initial content to load
    WebDriverWait(browser, 15).until(
        EC.presence_of_element_located((By.XPATH, "//div[starts-with(@id, 'showroom_')]"))
    )
    
    
    scroll_attempts = 0
    found = False
    
    while scroll_attempts < maxiumum_scroll_attempts and not found:
        # Scrolling down to find first paint
        target_elements = browser.find_elements(By.ID, f"showroom_{first_paint_id}")
        if target_elements:
            found = True
            print(f"Found target element: showroom_{first_paint_id}")
            break
        browser.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)
        scroll_attempts += 1
        time.sleep(1)  # Allow time for new content to load
    
    if not found:
        print(f"Could not find showroom_{first_paint_id} after {maxiumum_scroll_attempts} scrolls.")
        browser.quit()
    else:
        # Now extract all showroom items (including the target)
        showroom_items = browser.find_elements(By.XPATH, "//div[starts-with(@id, 'showroom_')]")
        paints = []
        for item in showroom_items:
            parent_link = item.find_element(By.XPATH, ".//a[contains(@class, 'aspect-ratio--tp')]")
            href = parent_link.get_attribute('href')
            item_id = item.get_attribute('id')
            paints.append({"ID": item_id, "URL": href,'Title': (href.split('/')[-1]).replace('-',' ')})
    browser.quit()
    return paints
    


with open("config.json") as f:
    config = json.load(f)
    url = config['profile_url']
    first = config['first_paint_id']
    max_scroll = config['maxiumum_scroll_attempts']
paints = get_all_showroom_paints(url,first,max_scroll)
def save_paint_image():
    pass