# Importing libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.options import Options

options = Options()
options.headless = True
options.binary = FirefoxBinary(r'/usr/bin/iceweasel')
driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(), options=options)
import os, json
from datetime import datetime
import logging
logging.basicConfig(format="%(name)s - %(levelname)s - %(message)s",
                    filename='/home/bitnami/htdocs/projects/TeslaSpectra/selenium/logs/Patent_App_check.log', level=logging.INFO)
dateTimeObj = datetime.now()

""" uses Selenium to go to the US Patent webpage search engine and scrape the
title of the most recent patent application name
"""


def checkPatent():
    website = 'https://appft.uspto.gov/netacgi/nph-Parser?Sect1=PTO2&Sect2=HITOFF&p=1&u=%2Fnetahtml%2FPTO%2Fsearch-bool.html&r=0&f=S&l=50&TERM1=Tesla%2C+Inc&FIELD1=&co1=AND&TERM2=&FIELD2=&d=PG01'

    driver.get(website)
    scrapedPatentTitle = driver.find_element(By.XPATH, '//tr[2]/td[3]').text
    datetimeObj = datetime.now()
    logging.info("process started--------------------------------------------")
    patentTitle = {
                'patentTitle': scrapedPatentTitle,
                'timeScraped': str(datetimeObj)}
    print("the scraped title is {}".format(patentTitle))
    logging.info("the scraped title is {}".format(patentTitle))
    referencePatentName = 'json/storedpatentname.json'

    if os.stat(referencePatentName).st_size == 0:
        with open('json/storedpatentname.json', 'w') as outfile:
            json.dump(patentTitle, outfile)
            logging.info("storepatentname file was empty, populating with latest scrape")

    else:
        with open('json/storedpatentname.json', 'r') as readfile:
            archivedPatent = json.load(readfile)

        print(archivedPatent["patentTitle"])
        logging.info("the archived patent title is: {}".format(archivedPatent["patentTitle"]))

        if scrapedPatentTitle == archivedPatent["patentTitle"]:
            print("There has been no new patent filing")
            logging.info("There has been no new patent filing")

        else:
            print("there has been a change to the webpage!")
            logging.info("there has been a change to the webpage!")
            #patent check will do all the work for us including appending to the newpatent.json file
            try:
                driver.get(website)
                top_patent_title = driver.find_element(By.XPATH, '//tr[2]/td[3]').text
                print("Tesla's most recent patent filing: {}".format(top_patent_title))

                link = driver.find_element(By.XPATH, '//tr[2]/td[3]')
                link.click()
                date_filed = driver.find_element(By.XPATH, '//table/tbody/tr[3]/td[2]/b').text
                abstract = driver.find_element(By.XPATH, '//body[@bgcolor="#FFFFFF"]/p[2]').text

                patentEntry = {'patent': top_patent_title,
                               'filing date': date_filed,
                               'abstract': abstract,
                               'scraped_at': str(dateTimeObj)}

                logging.info("Teslas most recent patent filing:{}".format(patentEntry))

                with open('json/newpatent.json', 'w') as outfile:
                    json.dump(patentEntry, outfile)

                with open('json/storedpatentname.json', 'w') as outfile:
                    json.dump(patentTitle, outfile)

            except Exception as e:
                print("error occured")
                logging.exception("an error occurred!")
            finally:
                driver.close()

checkPatent()
logging.info("process completed-------------------------------------------------")