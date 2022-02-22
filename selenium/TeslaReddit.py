from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.options import Options
options = Options()
options.headless = True
# options.binary = FirefoxBinary(r'/usr/bin/iceweasel')
import json
import logging
import os
import boto3
from Tesla import settings

#create  a connection to S3 using boto3 and the AWS access keys hidden in settings.py
s3 = boto3.client('s3', aws_access_key_id = settings.aws_access_key_id,
                  aws_secret_access_key= settings.aws_secret_access_key)

"""Convert relative to absolute paths to avoid conflict in crontab"""
script_path = os.path.abspath(__file__) # i.e. /path/to/selenium/script.py
script_dir = os.path.split(script_path)[0] #i.e. /path/to/selenium/

logging.basicConfig(format="%(name)s - %(levelname)s - %(message)s",
                    filename=script_dir + '/logs/TeslaReddit.log', level=logging.INFO)
dateTimeObj = datetime.now()

driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(), options=options)


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

            with open(script_dir + '/json/rTeslaMotors.json', 'w') as outfile:
                json.dump(TeslaMotors, outfile)
            with open(script_dir + "/json/rTeslaMotors.json", "rb") as f:
                s3.upload_fileobj(f, "teslaspectrajson", "rTeslaMotors.json")
            break
            logging.info("process completed------------------------------------------------------")


rTeslaMotors()

