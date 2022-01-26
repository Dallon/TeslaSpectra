# import all your stuff..
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
import time
dateTimeObj = datetime.now()


def rTeslaMotors():
    website = 'http://www.reddit.com/r/teslamotors'
    s = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=s, options=chrome_options)
    driver.get(website)

    firstPostTimeStamp = driver.find_element(By.XPATH, "//div[contains(@class, 'rpBJOH')]//"
                                                       "div[@data-testid='post-container']//a[@data-click-id='timestamp']").text
    splitString=firstPostTimeStamp.split()
    firstPostTimeStamp = splitString
    """The while loop checks for the presence of 'days' in the timestamp of 1st post, 
    re-assigning the variable firstPostTimeStamp to the next timestamp xpath if 'days' is found, and
     checking if there is 'days' on the new xpath again. If so, it continues reassigning the 
     variable until there is no longer 'days' in the timestamp. Then we know we've reached 
     the first 'Hot Post' of the past 24 hours"""

    PostNumber = 0
    while True:
        if firstPostTimeStamp[1] == "days":
            PostNumber = PostNumber + 1
            firstPostTimeStamp = driver.find_element(By.XPATH, "(//div[contains(@class, 'rpBJOH')]//"
            "div[@data-testid='post-container']//a[@data-click-id='timestamp'])[{}]".format(PostNumber)).text
            new_Var = firstPostTimeStamp.split()
            firstPostTimeStamp = new_Var

        # Because PostNumber represents the index number of the post we can use it to gather
        # the relevant post data
        else:
            firstPostTitle = driver.find_element(By.XPATH, "(//div[contains(@class, 'rpBJOH')]//"
             "div[@data-testid='post-container']//h3)[{}]".format(PostNumber)).text
            # print(firstPostTitle)
            firstPostUpvotes = driver.find_element(By.XPATH, "(//div[contains(@class, 'rpBJOH')]//"
             "div[@data-testid='post-container'])[{}]//div[contains(@id, 'vote-arrows')]".format(PostNumber)).text

            #the if statement below allows us to view the upvotes as a number.
            if "." in firstPostUpvotes:
                firstPostUpvotes = firstPostUpvotes.replace("k", "00").replace(".", "")
            #if there are no votes, the votes placeholder says Vote. we need to change that
            #to avoid an error.
            if firstPostUpvotes =='Vote':
                firstPostUpvotes = 0

            if int(firstPostUpvotes) > 500:
                hotPost = 'Super Hot'
            else:
                hotPost = ''

            # print(firstPostUpvotes)

            rTeslaMotors = {'postTitle': firstPostTitle,
                            'postUpvotes': firstPostUpvotes,
                            'hotPost': hotPost,}


            with open ('rTeslaMotors.json', 'w') as outfile:
                json.dump(rTeslaMotors, outfile)
            break




rTeslaMotors()
