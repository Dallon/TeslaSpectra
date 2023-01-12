from selenium.webdriver.common.by import By
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


#this function assumes you have already populated the json file with a dictionary containing
#scraped patent details
logging.basicConfig(filename='logs/Patent_App_check.log', filemode='w',
                    format='%(asctime)s - %(message)s', level=logging.INFO)


def store_patent_info(driver, patentEntry):

    with open(script_dir + '/json/scrapedpatents.json', 'r') as readfile:
        archivedPatent = json.load(readfile)
    newPatentScraped = False
    for i in range(1, 5):
        #in case there is more than one patent published in a day, iterate through the rows
        # in column 14 in the table shown, comparing the previously scraped title stored in
        # our json file with the newly scraped title
        patentTitle = driver.find_element(By.XPATH, "(//div[@data-cell=14])[{}]".format(i)).text
        # print(archivedPatent["patentTitle"])
        # print(archivedPatent["patent{}".format(i)])
        # Check if patentTitle just scraped is already in archivedPatent
        already_scraped = False
        for value in archivedPatent.values():
            if value == patentTitle:
                already_scraped = True
                break

        if already_scraped:
            print("There has been no new patent published")
            break

        else:
            print("there has been a new patent published!")
            patentPublishDate = driver.find_element(By.XPATH, "(//div[@data-cell=11])[{}]".format(i)).text
            print(patentPublishDate)
            patentDocButton = driver.find_element(By.XPATH, "(//div[@data-cell=10])[{}]".format(i))
            patentDocButton.click()
            time.sleep(3)
            #once the doc button is clicked we can scrape the abstract from the now visible patent document
            patentAbstract = driver.find_element(By.XPATH, "//p[@data-section = "
                                                           "'abstract' and @id = '3']").text
            patentEntry["patent{}".format(i)] = patentTitle
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

