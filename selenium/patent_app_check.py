# Importing libraries
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support.ui import Select
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from store_patent_info import store_patent_info
options = Options()
options.headless = False
options.binary = FirefoxBinary(r'/usr/bin/iceweasel')


""" uses Selenium to go to the US Patent webpage search engine and scrape the
title of the most recent patent application name
"""
s = Service(GeckoDriverManager().install())
driver = webdriver.Firefox(service=s, options=options)


def checkPatent():
    try:
        website = 'https://ppubs.uspto.gov/pubwebapp/'
        driver.get(website)
        time.sleep(5)

        # initialize the input search textbox
        inputText = driver.find_element(By.CLASS_NAME, "trix")
        selectAllDBsButton = driver.find_element(By.ID, "allDBs")
        USPatDBSelect = driver.find_element(By.ID, "USPAT")
        searchDefaultOperator = Select(driver.find_element(By.CLASS_NAME, "operator"))
        selectAllDBsButton.click()
        USPatDBSelect.click()
        searchDefaultOperator.select_by_value("SAME")
        inputText.click()
        inputText.send_keys("Tesla, Inc"[::-1])
        searchButton = driver.find_element(By.ID, "search-btn-search")
        searchButton.click()
        time.sleep(10)

        patentEntry = {}
        #now that we have clicked search and made our empty dict
        # we can start initializing some patent web element variables
        store_patent_info(driver, patentEntry)
        # print(patentsOfToday)
    except Exception as e:
        # print(e)
        # print("exception")
        logging.exception(e)
    finally:
        logging.info("process completed-------------------------------------------------")
        driver.close()
        driver.quit()

checkPatent()