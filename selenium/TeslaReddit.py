from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from datetime import datetime
import json
import time
import os
import schedule
import logging
logging.basicConfig(format="%(name)s - %(levelname)s - %(message)s",
                    filename='logs/TeslaReddit.log', level=logging.INFO)
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
dateTimeObj = datetime.now()
s = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(options=chrome_options)


def rTeslaMotors():
    logging.info("process started-------------------------------------------------------------")
    website = 'http://www.reddit.com/r/teslamotors'
    driver.get(website)
    firstPostTimeStamp = driver.find_element(By.XPATH, "//div[contains(@class, 'rpBJOH')]//"
        "div[@data-testid='post-container']//a[@data-click-id='timestamp']").text
    splitString = firstPostTimeStamp.split()
    firstPostTimeStamp = splitString
    print(splitString)

    """The while loop below checks for the presence of 'days', 'months' etc in the timestamp of the 1st post, 
    re-assigning the variable firstPostTimeStamp to the next timestamp xpath if 'days' is found.
     Then checking if there is 'days', 'months' etc on the new xpath, and if so it continues reassigning the 
     variable until there is no longer 'days' etc in the timestamp. Then we know we've reached 
     the first 'Hot Post' of the past 24 hours"""
    postNumber = 1
    while True:
        if firstPostTimeStamp[1] == "days" or firstPostTimeStamp[1] == "day" \
                or firstPostTimeStamp[1] == "month" or firstPostTimeStamp[1] == "months":
            postNumber = postNumber + 1
            firstPostTimeStamp = driver.find_element(By.XPATH, "(//div[contains(@class, 'rpBJOH')]//"
    "div[@data-testid='post-container']//a[@data-click-id='timestamp'])[{}]".format(postNumber)).text
            new_Var = firstPostTimeStamp.split()
            firstPostTimeStamp = new_Var
            print(firstPostTimeStamp)
        # Because PostNumber represents the index number of the post we can use it to gather
        # the relevant post data
        else:
            firstPostTitle = driver.find_element(By.XPATH, "(//div[contains(@class, 'rpBJOH')]//"
             "div[@data-testid='post-container']//h3)[{}]".format(postNumber)).text
            print(firstPostTitle)
            logging.info("first post title logged as {}".format(firstPostTitle))
            firstPostUpvotes = driver.find_element(By.XPATH, "(//div[contains(@class, 'rpBJOH')]//"
             "div[@data-testid='post-container'])[{}]//div[contains(@id, 'vote-arrows')]".format(postNumber)).text

            #the if statement below allows us to view the upvotes as a number.
            if "." in firstPostUpvotes:
                firstPostUpvotes = firstPostUpvotes.replace("k", "00").replace(".", "")

            #if there are no votes, the votes placeholder says Vote. we need to change that
            #to avoid an error.
            if firstPostUpvotes == 'Vote':
                firstPostUpvotes = 0

            logging.info("upvotes logged as {}".format(firstPostUpvotes))

            if int(firstPostUpvotes) > 500:
                hotPost = 'Super Hot'
            else:
                hotPost = ''

            TeslaMotors = {'postTitle': firstPostTitle,
                         'postUpvotes': firstPostUpvotes,
                         'hotPost': hotPost,
                         'scraped_at': str(dateTimeObj)}

            logging.info("scraped data logged: {}".format(TeslaMotors))

            with open('json/rTeslaMotors.json', 'w') as outfile:
                json.dump(TeslaMotors, outfile)
            break
            logging.info("process completed------------------------------------------------------")


rTeslaMotors()

