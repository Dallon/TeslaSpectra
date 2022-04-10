from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
options = Options()
options.headless = True
options.binary = FirefoxBinary(r'/usr/bin/iceweasel')
options.log.level = "trace"
import json
import logging
import os
import boto3
from logs import secretkeys
#Convert relative to absolute paths to avoid conflict in crontab
script_path = os.path.abspath(__file__) # i.e. /path/to/selenium/script.py
script_dir = os.path.split(script_path)[0] #i.e. /path/to/selenium/

#create  a connection to S3 using boto3 and the AWS access keys hidden in settings.py
s3 = boto3.client('s3', aws_access_key_id=secretkeys.aws_access_key_id,
                  aws_secret_access_key=secretkeys.aws_secret_access_key)

dateTimeObj = datetime.now()
driver = GeckoDriverManager().install()
# print("driver has been assigned to GeckoDriverManager().install()")
s = Service(driver)
driver = webdriver.Firefox(service=s, options=options)
# print("webdriver loaded")


def rTeslaMotors():
    website = 'http://www.reddit.com/r/teslamotors'
    driver.get(website)
    postTimeStamp = driver.find_element(By.XPATH, "//div[contains(@class, 'rpBJOH')]//"
        "div[@data-testid='post-container']//a[@data-click-id='timestamp']").text
    splitString = postTimeStamp.split()
    postTimeStamp = splitString
    # print("Confirm scaper works by taking first listed post's timestamp and displaying it:" + str(splitString))

    """The while loop below checks for the presence of 'hours' in the timestamp of the 1st post, 
    re-assigning the variable firstPostTimeStamp to the next timestamp xpath if 'hours' is not found. if hours not found
     it continues reassigning the variable until there is 'hours' in the timestamp. Then we know we've 
    reached the most upvoted OR the first pinned post of the past 24 hours"""
    postNumber = 0
    while True:
        if postTimeStamp[1] != 'hours':
            postNumber = postNumber + 1
            postTimeStamp = driver.find_element(By.XPATH, "(//div[contains(@class, 'rpBJOH')]//"
    "div[@data-testid='post-container']//a[@data-click-id='timestamp'])[{}]".format(postNumber)).text
            postTimeStamp = postTimeStamp.split()
            # print("The #{} post's timestamp is:".format(postNumber) + str(postTimeStamp))
        else:
        # Because PostNumber represents the index number of the post we can use it to gather
        # the relevant post data
            try:
                firstPostTitle = driver.find_element(By.XPATH, "(//div[contains(@class, 'rpBJOH')]//"
                 "div[@data-testid='post-container']//h3)[{}]".format(postNumber)).text
                # print("the #{} post timestamp contains {}"
    # " making it the first hot post of the day".format(postNumber,postTimeStamp[1]))

                print("The first hot post Title is: {}".format(firstPostTitle))
                Upvotes = driver.find_element(By.XPATH, "(//div[contains(@class, 'rpBJOH')]//"
                 "div[@data-testid='post-container'])[{}]//div[contains(@id, 'vote-arrows')]".format(postNumber)).text
                print("The upvotes were sucessfully scraped at: {}".format(Upvotes))
                postlink = driver.find_element(By.XPATH, "(//div[contains(@class, 'rpBJOH')]//"
                "div[@data-testid='post-container'])[{}]//a[@data-click-id='body']".format(
                    postNumber)).get_attribute("href")

                #the if statement below allows us to view the upvotes as a number.
                if "." in Upvotes:
                    Upvotes = Upvotes.replace("k", "00").replace(".", "")

                #if there are no votes, the votes placeholder says Vote. we need to change that
                #to avoid an error.
                if Upvotes == 'Vote':
                    Upvotes = 0

                if 100 < int(Upvotes) <= 1000:
                    storedUpvotes = "{}00+".format(str(Upvotes)[0])
                    hotPost = ''
                elif int(Upvotes) > 1000:
                    hotPost = ''
                    storedUpvotes = "{}{}00+".format(str(Upvotes)[0], str(Upvotes)[1])
                elif int(Upvotes) > 4000:
                    hotpost = 'Hot'
                else:
                    storedUpvotes = "{}0+".format(str(Upvotes)[0])
                    hotPost = ''

                newscraped = {'postTitle': firstPostTitle,
                             'postUpvotes': storedUpvotes,
                             'hotPost': hotPost,
                             'scraped_at': str(dateTimeObj),
                              "postLink":postlink}


                with open(script_dir + '/json/rTeslaMotors.json', 'w') as outfile:
                    json.dump(newscraped, outfile)
                # print("r/TeslaMotors local JSON populated")
                logging.info("r/TeslaMotors local JSON populated")
                with open(script_dir + "/json/rTeslaMotors.json", "rb") as f:
                    s3.upload_fileobj(f, "teslaspectrajson", "rTeslaMotors.json")
                # print("r/TeslaMotors S3 JSON populated")
                logging.info("r/TeslaMotors S3 JSON populated")

            except Exception as e:
                print(e)
                logging.exception(e)
            finally:
                driver.quit()
                print("driver quit")
                logging.info("driver.quit")
                break #due to while true loop if we don't break the program doesn't end

rTeslaMotors()

