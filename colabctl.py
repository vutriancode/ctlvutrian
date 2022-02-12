import sys
sys.path.insert(0,'/usr/bin/chromedriver')
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pickle
import time
import validators
from Settings import *
from pymongo import MongoClient
account  = MongoClient(CONNECTION_STRING_MGA1).cookie[MAY]
def sleep(seconds):
    for i in range(seconds):
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            continue


def exists_by_text2(driver, text):
    try:
        WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH,"//*[contains(text(), '"+str(text)+"')]")))
    except Exception:
        return False
    return True


def exists_by_xpath(driver, thex, howlong):
    try:
        WebDriverWait(driver, howlong).until(ec.visibility_of_element_located((By.XPATH, thex)))
    except:
        return False


def exists_by_text(driver, text):
    driver.implicitly_wait(2)
    try:
        driver.find_element_by_xpath("//*[contains(text(), '"+str(text)+"')]")
    except NoSuchElementException:
        driver.implicitly_wait(5)
        return False
    driver.implicitly_wait(5)
    return True


def user_logged_in(driver):
    try:
        driver.find_element_by_xpath('//*[@id="file-type"]')
    except NoSuchElementException:
        driver.implicitly_wait(5)
        return False
    driver.implicitly_wait(5)
    return True


def wait_for_xpath(driver, x):
    while True:
        try:
            driver.find_element_by_xpath(x)
            return True
        except:
            time.sleep(0.1)
            pass


def scroll_to_bottom(driver):
    SCROLL_PAUSE_TIME = 0.5
    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


def file_to_list(filename):
    colabs = []
    for line in open(filename):
        if validators.url(line):
            colabs.append(line)
    return colabs


def switch_to_tab(driver, tab_index):
    print("Switching to tab " + str(tab_index))
    try:
        driver.switch_to.window(driver.window_handles[tab_index])
    except:
        print("Error switching tabs.")
        return False


def new_tab(driver, url, tab_index):
    if tab_index+1>len(driver.window_handles):

        print("Opening new tab to " + str(url))
        try:
            driver.execute_script("window.open('');")
            switch_to_tab(driver, tab_index)

            driver.get(url)

        except Exception as e:
            print(e)
            print("Error opening new tab.")
            return False
        switch_to_tab(driver, tab_index)
    else:
        switch_to_tab(driver, tab_index)
    return True
def new_tab1(driver, url, tab_index):
    if tab_index+1>len(driver.window_handles):

        print("Opening new tab to " + str(url))
        try:
            driver.execute_script("window.open('');")
            switch_to_tab(driver, tab_index)

            driver.get(url)

        except Exception as e:
            print(e)
            print("Error opening new tab.")
            return False
        switch_to_tab(driver, tab_index)
    else:
        switch_to_tab(driver, tab_index)
        driver.get(url)
    return True
    

colab_urls = file_to_list('notebooks.csv')

if len(colab_urls) > 0 and validators.url(colab_urls[0]):
    colab_1 = colab_urls[0]
else:
    raise Exception('No notebooks')

chrome_options = Options()
chrome_options.add_argument('--headless') # uncomment for headless mode
chrome_options.add_argument('--no-sandbox')
#chrome_options.add_argument("user-data-dir=profile") # left for debugging
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--disable-infobars')
chrome_options_gui = Options()
chrome_options_gui.add_argument('--no-sandbox')
#chrome_options.add_argument("user-data-dir=profile") # left for debugging
chrome_options_gui.add_argument('--disable-infobars')
chrome_options_gui.add_argument('--disable-gpu')

cookies = account.find().limit(5)
cookiess = []
for i in cookies:
    cookiess.append(i)
wds = []
print(cookiess)
for cookies in cookiess:
    wd = webdriver.Chrome(LINK_DRIVE, options=chrome_options_gui)


    wd.get("https://google.com")
    time.sleep(2)

    wd.get("https://accounts.google.com")
    time.sleep(2)

    wd.get("https://colab.research.google.com")
    time.sleep(3)
    try:
        for cookie in cookies["cookie"]:
            if cookie["domain"] != "myaccount.google.com":
                print(cookie)

                wd.add_cookie(cookie)
    except Exception:
        pass
    for index,colab_url in enumerate(cookies["listurl"]):
        complete = False
        print(colab_url)
        new_tab1(wd,colab_url,index)

        print("Logged in.") # for debugging
        running = False
        wait_for_xpath(wd, '//*[@id="file-menu-button"]/div/div/div[1]')
        print('Notebook loaded.')
        sleep(10)
        webdriver.ActionChains(wd).key_down(Keys.CONTROL).send_keys(Keys.F9).perform()

        # while not exists_by_text(wd, "Sign in"):
        if exists_by_text(wd, "Runtime disconnected"):
            try:
                wd.find_element_by_xpath('//*[@id="ok"]').click()
            except NoSuchElementException:
                pass
        if exists_by_text2(wd, "Notebook loading error"):
            wd.get(colab_url)
        try:
            wd.find_element_by_xpath('//*[@id="file-menu-button"]/div/div/div[1]')
            if not running:
                wd.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.SHIFT + "q")
                wd.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.SHIFT + "k")
                exists_by_xpath(wd, '//*[@id="ok"]', 10)
                wd.find_element_by_xpath('//*[@id="ok"]').click()
                sleep(10)
                wd.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.F9)
                running = True
        except NoSuchElementException:
            pass
        if running:
            try:
                wd.find_element_by_css_selector('.notebook-content-background').click()
                #actions = ActionChains(wd)
                #actions.send_keys(Keys.SPACE).perform()
                scroll_to_bottom(wd)
                print("performed scroll")
            except:
                pass
            for frame in wd.find_elements_by_tag_name('iframe'):
                wd.switch_to.frame(frame)
                '''
                links = browser.find_elements_by_partial_link_text('oauth2/auth')
                for link in links:
                    new_tab(wd, link.get_attribute("href"), 1)
                    wd.find_element_by_css_selector('li.M8HEDc:nth-child(1)>div:nth-child(1)').click()
                    wd.find_element_by_css_selector('#submit_approve_access>content:nth-child(3)>span:nth-child(1)').click()
                    auth_code = wd.find_element_by_xpath('/html/body/div[1]/div[1]/div[2]/div[2]/div/div/div[2]/div/div/div/form/content/section/div/content/div/div/div/textarea').text
                '''
                wd.switch_to.default_content()
                if complete:
                    break
                # if complete:
                #     break
    wds.append(wd)

while True:
    for index, wd in enumerate(wds):
        for index,colab_url in enumerate(cookiess[index]["listurl"]):
            complete = False
            new_tab(wd,colab_url,index)

            print("Logged in.") # for debugging
            running = True
            wait_for_xpath(wd, '//*[@id="file-menu-button"]/div/div/div[1]')
            print('Notebook loaded.')
            sleep(10)
            webdriver.ActionChains(wd).key_down(Keys.CONTROL).send_keys(Keys.F9).perform()

            # while not exists_by_text(wd, "Sign in"):
            if exists_by_text(wd, "Runtime disconnected"):
                try:
                    wd.find_element_by_xpath('//*[@id="ok"]').click()
                except NoSuchElementException:
                    pass
            if exists_by_text2(wd, "Notebook loading error"):
                running = False

                wd.get(colab_url)
            try:
                wd.find_element_by_xpath('//*[@id="file-menu-button"]/div/div/div[1]')
                if not running:
                    wd.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.SHIFT + "q")
                    wd.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.SHIFT + "k")
                    exists_by_xpath(wd, '//*[@id="ok"]', 10)
                    wd.find_element_by_xpath('//*[@id="ok"]').click()
                    sleep(10)
                    wd.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.F9)
                    running = True
            except NoSuchElementException:
                pass
            if running:
                try:
                    wd.find_element_by_css_selector('.notebook-content-background').click()
                    #actions = ActionChains(wd)
                    #actions.send_keys(Keys.SPACE).perform()
                    scroll_to_bottom(wd)
                    print("performed scroll")
                except:
                    pass
                for frame in wd.find_elements_by_tag_name('iframe'):
                    wd.switch_to.frame(frame)
                    '''
                    links = browser.find_elements_by_partial_link_text('oauth2/auth')
                    for link in links:
                        new_tab(wd, link.get_attribute("href"), 1)
                        wd.find_element_by_css_selector('li.M8HEDc:nth-child(1)>div:nth-child(1)').click()
                        wd.find_element_by_css_selector('#submit_approve_access>content:nth-child(3)>span:nth-child(1)').click()
                        auth_code = wd.find_element_by_xpath('/html/body/div[1]/div[1]/div[2]/div[2]/div/div/div[2]/div/div/div/form/content/section/div/content/div/div/div/textarea').text
                    '''
                    wd.switch_to.default_content()
                    if complete:
                        break
                # if complete:
                #     break
