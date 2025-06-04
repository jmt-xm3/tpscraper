from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import json
import os
import urllib.request

def get_all_showroom_paints(profile_url,first_paint_id,maxiumum_scroll_attempts):
    """_This is a function that opens firefox reads a trading paints profile and saves the hyperlinks,
    the ID and the title of each paint. To do this is pages down to load all the content until it finds the first upload specified by config file _

    Args:
        profile_url (_type_): _String - trading paints profile url eg https://www.tradingpaints.com/profile/858183/Jonan-Turner_
        first_paint_id (_type_): _The first paint ID it is found after /view/ in the url eg 933999 from https://www.tradingpaints.com/showroom/view/933999/REVSPORT-International-X-ARCA-Ford-Mustang  _
        maxiumum_scroll_attempts (_type_): _Maximum ammount of scrolls before browser times out set in config file set higher if you have a lot of paints on your profile_

    Returns:
        _type_: _description_
    """
    browser = webdriver.Chrome()
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
        showroom_items = browser.find_elements(By.XPATH, "//div[starts-with(@id, 'showroom_') and substring(@id, string-length(@id), 1) >= '0' and substring(@id, string-length(@id), 1) <= '9']")
        paints = []
        for item in showroom_items:
            parent_link = item.find_element(By.XPATH, ".//a[contains(@class, 'aspect-ratio--tp')]")
            href = parent_link.get_attribute('href')
            item_id = item.get_attribute('id')
            print("ID:",item_id,"Title:",(href.split('/')[-1]).replace('-',' '))
            paints.append({"id": item_id, "url": href,'title': (href.split('/')[-1]).replace('-',' '),"assset": None})
    browser.quit()
    return paints
    

def save_images(url,title):
    try:
        os.mkdir(title)
    except FileExistsError:
        pass
    full_path = os.path.join(title,'preview.jpg')
    urllib.urlretrieve(url, full_path)

def find_preview_image_url(paint):
      browser = webdriver.Firefox()
      url = paint['url']
      browser.get(url)
      WebDriverWait(browser, 10)

with open("config.json") as f:
    config = json.load(f)
    url = config['profile_url']
    first = config['first_paint_id']
    max_scroll = config['maxiumum_scroll_attempts']


def save_paints_to_json(paints):
    paints_json = json.dumps(paints)
    with open('paints.json', 'w') as f:
        json.dump(paints_json, f)

paints = get_all_showroom_paints(url,first,max_scroll)
save_paints_to_json(paints)

