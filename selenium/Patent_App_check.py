# Importing libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service

options = Options()
options.headless = True
options.binary = FirefoxBinary(r'/usr/bin/iceweasel')
import os, json
from datetime import datetime
import logging
import boto3
from logs import secretkeys

#Convert relative to absolute paths to avoid conflict in crontab
script_path = os.path.abspath(__file__) # i.e. /path/to/selenium/script.py
script_dir = os.path.split(script_path)[0] #i.e. /path/to/selenium/

dateTimeObj = datetime.now()

# create  a connection to S3 using boto3 and the AWS access keys hidden in settings.py
s3 = boto3.client('s3', aws_access_key_id=secretkeys.aws_access_key_id,
                  aws_secret_access_key=secretkeys.aws_secret_access_key)


""" uses Selenium to go to the US Patent webpage search engine and scrape the
title of the most recent patent application name
"""
s = Service(GeckoDriverManager().install())
driver = webdriver.Firefox(service=s, options=options)


def checkPatent():
    website = 'https://appft.uspto.gov/netacgi/nph-Parser?Sect1=PTO2&Sect2=HITOFF&p=1&u=%2Fnetahtml%2FPTO%2Fsearch-bool.html&r=0&f=S&l=50&TERM1=Tesla%2C+Inc&FIELD1=&co1=AND&TERM2=&FIELD2=&d=PG01'

    driver.get(website)
    scrapedPatentTitle = driver.find_element(By.XPATH, '//tr[2]/td[3]').text
    datetimeObj = datetime.now()
    patentTitle = {
                'patentTitle': scrapedPatentTitle,
                'timeScraped': str(datetimeObj)}
    # print("the scraped title is {}".format(patentTitle))
    referencePatentName = '/json/storedpatentname.json'

    if os.stat(script_dir + referencePatentName).st_size == 0:
        with open(script_dir + '/json/storedpatentname.json', 'w') as outfile:
            json.dump(patentTitle, outfile)

        with open(script_dir + "/json/storedpatentname.json", "rb") as f:
            s3.upload_fileobj(f, "teslaspectrajson", "storedpatentname.json")

    else:
        with open(script_dir + '/json/storedpatentname.json', 'r') as readfile:
            archivedPatent = json.load(readfile)

        # print(archivedPatent["patentTitle"])

        if scrapedPatentTitle == archivedPatent["patentTitle"]:
            print("There has been no new patent filing")

        else:
            print("there has been a new patent filing!!")
            #patent check will do all the work for us including appending to the newpatent.json file
            try:
                driver.get(website)
                top_patent_title = driver.find_element(By.XPATH, '//tr[2]/td[3]').text
                print("Tesla's most recent patent filing: {}".format(top_patent_title))

                link = driver.find_element(By.XPATH, '//tr[2]/td[3]/a')
                link.click()
                date_filed = driver.find_element(By.XPATH, '//table/tbody/tr[3]/td[2]/b').text
                abstract = driver.find_element(By.XPATH, '//body[@bgcolor="#FFFFFF"]/p[2]').text

                patentEntry = {'patent': top_patent_title,
                               'filing date': date_filed,
                               'abstract': abstract,
                               'scraped_at': str(dateTimeObj)}

                with open(script_dir + '/json/newpatent.json', 'w') as outfile:
                    json.dump(patentEntry, outfile)

                with open(script_dir + "/json/newpatent.json", "rb") as f:
                    s3.upload_fileobj(f, "teslaspectrajson", "newpatent.json")

                with open(script_dir + '/json/storedpatentname.json', 'w') as outfile:
                    json.dump(patentTitle, outfile)

                with open(script_dir + "/json/storedpatentname.json", "rb") as f:
                    s3.upload_fileobj(f, "teslaspectrajson", "storedpatentname.json")
            except Exception as e:
                print(e)

            finally:
                driver.quit()
                print(driver.quit)

checkPatent()
logging.info("process completed-------------------------------------------------")