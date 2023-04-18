from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import os
import json
import time
import boto3
import logging
from logs import secretkeys
#Convert relative to absolute paths to avoid conflict in crontab
script_path = os.path.abspath(__file__)  # i.e. /path/to/scrapers/script.py
script_dir = os.path.split(script_path)[0]  #i.e. /path/to/scrapers/

# create  a connection to S3 using boto3 and the AWS access keys hidden in settings.py
s3 = boto3.client('s3', aws_access_key_id=secretkeys.aws_access_key_id,
                  aws_secret_access_key=secretkeys.aws_secret_access_key)



logging.basicConfig(filename='logs/Patent_App_check.log', filemode='w',
                    format='%(asctime)s - %(message)s', level=logging.INFO)

#this function assumes you have already populated the json file with a dictionary containing
#scraped patent details


def store_patent_info(driver, patentEntry):

    with open(script_dir + '/json/scrapedpatents.json', 'r') as readfile:
        archivedPatent = json.load(readfile)
    newPatentScraped = False
    # Wait for the search results to load using WebDriverWait and check for presence of the 1st row of
    #cell 14 to load.
    try:
        wait = WebDriverWait(driver, 100)
        wait.until(EC.presence_of_element_located((By.XPATH, "(//div[@data-cell=14])[1]")))

    except TimeoutException:
        print("Search results not found within timeout period of 100 seconds")
    for i in range(1, 5):

        #in case there is more than one patent published in a day, iterate through the rows
        # in column 14 in the table shown, comparing the previously scraped title stored in
        # our json file with the newly scraped title

        scraped_patent_title = driver.find_element(By.XPATH, "(//div[@data-cell=14])[{}]".format(i)).text

        # print(archivedPatent["patent{}".format(i)])
        # Check if scraped_patent_title just scraped is already in archivedPatent.

        already_scraped = False

        for value in archivedPatent.values():
            # If scraped_patent_title is already in archivedPatent, we don't need to look any further
            # because the patents are in descending order of date published.
            if scraped_patent_title == value:
                already_scraped = True
                break

        if already_scraped:
            # print("There has been no new patent published")
            logging.info("There has been no new patent published since " + scraped_patent_title)
            break

        else:
            # print("there has been a new patent published!")
            logging.info("there has been a new patent published!")
            patentPublishDate = driver.find_element(By.XPATH, "(//div[@data-cell=11])[{}]".format(i)).text
            # print(patentPublishDate)
            logging.info(patentPublishDate)
            patentDocButton = driver.find_element(By.XPATH, "(//div[@data-cell=10])[{}]".format(i))
            patentDocButton.click()
            #wait for presence of loaded patent document
            try:
                wait = WebDriverWait(driver, 100)
                wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class= 'docMetadata']")))

            except TimeoutException:
                print("Patent document not found within timeout period of 100 seconds")
            #once the doc button is clicked and the document is loaded
            # we can scrape the abstract from the now visible patent document if its there, otherwise
            #we will assign the text  value of "No Abstract" to the patentAbstract

            try:
                patentAbstract = driver.find_element(By.XPATH, "//p[@data-section='abstract' and @id='3']").text
            except NoSuchElementException:
                patentAbstract = "No Abstract"

            patentEntry["patent{}".format(i)] = scraped_patent_title
            patentEntry["publishing date{}".format(i)] = patentPublishDate
            patentEntry["abstract{}".format(i)] = patentAbstract
            newPatentScraped = True

    if newPatentScraped:
        with open(script_dir + '/json/scrapedpatents.json', 'w') as outfile:
            json.dump(patentEntry, outfile)

        with open(script_dir + "/json/scrapedpatents.json", "rb") as f:
            s3.upload_fileobj(f, "teslaspectrajson", "scrapedpatents.json")
            logging.info("new patent details uploaded to S3")

    logging.info("end of helper function")