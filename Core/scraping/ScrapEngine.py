from selenium import webdriver
from bs4 import BeautifulSoup
# from urllib.parse import urljoin
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import os


class NoProductFoundException(Exception):
    pass





def connectToStaticWebSite(url, ignoreTerm=None):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--headless")
    options.add_argument("disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument('--log-level=3')
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    content = driver.page_source
    driver.close()
    soup = BeautifulSoup(content, features="html.parser")
    return soup

def connectToWebsiteWithBtnClick(url, buttonClass):
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--headless")
    options.add_argument("disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument('--log-level=3')
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    try:
        counter = 0
        while counter < 10:
            wait = WebDriverWait(driver, 10)
            element = wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "loadingcover")))
            btn = driver.find_element_by_class_name(buttonClass)
            #ActionChains(driver).move_to_element(btn).click().perform()
            btn.click()
            time.sleep(3)
            counter += 1
    except NoSuchElementException:
        print("Process {} pages".format(counter))
        pass
    except Exception as e:
        print("Error " + str(e))

    content = driver.page_source
    driver.close()
    soup = BeautifulSoup(content, features="html.parser")
    return soup

def processString(a: str, ignoreTerm):
    temp = a.lstrip()
    if ignoreTerm is not None:
        for term in ignoreTerm:
            temp = temp.replace(term, "")
    temp = temp.rstrip()
    return temp


def hideInvalidTag(originalContent, invalidTag:[str]):
    for tag in invalidTag:
        [x.extract() for x in originalContent.findAll(tag)]
    return originalContent
