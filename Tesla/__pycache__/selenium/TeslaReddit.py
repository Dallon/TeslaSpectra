#import all your stuff..
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
from selenium.webdriver.common.by import By
import os
from datetime import datetime
import json
dateTimeObj = datetime.now()


def rTeslaMotors():
    website = 'http://www.reddit.com/r/teslamotors'
    s = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=s, options=chrome_options)
    driver.get(website)
    #test_var below doesnt work because you aren't logged into reddit. Create a new path which
    #doesn't require being logged in.

    firstPostTitle = driver.find_element(By.XPATH, "//*[@id='t3_s290ru']/div[3]/div[2]/div[2]/a/div/h3").text
    firstPostUpvotes = driver.find_element(By.XPATH, "//*[@id='vote-arrows-t3_s290ru']/div").text

    if "." in firstPostUpvotes:
        firstPostUpvotes = firstPostUpvotes.replace("k", "00").replace(".", "")

    print(firstPostTitle)
    print(firstPostUpvotes)

rTeslaMotors()