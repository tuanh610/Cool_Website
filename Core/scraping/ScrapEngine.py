from selenium import webdriver
from bs4 import BeautifulSoup
# from urllib.parse import urljoin
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from Core.scraping.HoangHaMobileScraper import HoangHaMobileScraper
from Core.scraping.TheGioiDiDongScaper import TheGioiDiDongScraper
import os


class NoProductFoundException(Exception):
    pass


parser = {"hoanghaMobile": HoangHaMobileScraper, 'thegioididong': TheGioiDiDongScraper}


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

def connectToWebsiteWithBtnClick(url, buttonId):
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
            btn = driver.find_element_by_class_name(buttonId)
            btn.click()
            counter+=1
    except NoSuchElementException:
        pass
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
