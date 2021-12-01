import sys
sys.path.insert(0,'C:/Users/Admin/Desktop/chromedriver')
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
        driver.get(str(url))
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
for i in range(5):
    options = Options()
    options.add_argument("start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    #chrome_options.add_argument("user-data-dir=profile") # left for debugging
    options.add_argument('--disable-infobars')
    wd = webdriver.Chrome("C:/Users/Admin/Desktop/chromedriver", options=options)
    from selenium_stealth import stealth

    stealth(wd,
            languages=["vi-VN", "vi"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            )
    try:
        for cookie in pickle.load(open("gCookies.pkl", "rb")):
            if cookie["domain"] != "myaccount.google.com":
                print(cookie)

                wd.add_cookie(cookie)
    except Exception:
        pass
    wd.get(colab_1)
    time.sleep(30)
    pickle.dump(wd.get_cookies(), open("gCookies.pkl", "wb"))
    wd.close()
    wd.quit()
