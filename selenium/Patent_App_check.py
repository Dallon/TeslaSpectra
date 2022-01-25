# Importing libraries
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.add_argument("--disable-gpu")
# chrome_options.add_argument("--headless")
from selenium.webdriver.common.by import By
import schedule, os, time, json
from datetime import datetime

dateTimeObj = datetime.now()

""" uses Selenium to go to the US Patent webpage search engine and scrape the
title of the most recent patent application name
"""

# setting the URL you want to monitor(with urllib not selenium)
def checkPatent():
    website = 'https://appft.uspto.gov/netacgi/nph-Parser?Sect1=PTO2&Sect2=HITOFF&p=1&u=%2Fnetahtml%2FPTO%2Fsearch-bool.html&r=0&f=S&l=50&TERM1=Tesla%2C+Inc&FIELD1=&co1=AND&TERM2=&FIELD2=&d=PG01'
    s = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(options=chrome_options, service=s)
    # try:
    driver.get(website)
    scrapedPatentTitle = driver.find_element(By.XPATH, '//tr[2]/td[3]').text
    datetimeObj = datetime.now()
    patentTitle = {
                'patentTitle': scrapedPatentTitle,
                'timeScraped': str(datetimeObj)}

    referencePatentName = 'storedpatentname.json'

    if os.stat(referencePatentName).st_size == 0:
        with open('storedpatentname.json', 'w') as outfile:
            json.dump(patentTitle, outfile)

    else:
        with open('storedpatentname.json', 'r') as readfile:
            archivedPatent = json.load(readfile)

        print(archivedPatent["patentTitle"])

        if scrapedPatentTitle == archivedPatent["patentTitle"]:
            print("There has been no new patent filing")

        else:
            print("there has been a change to the webpage!")
            #patent check will do all the work for us including appending to the newpatent.json file
            try:
                driver.get(website)
                top_patent_title = driver.find_element(By.XPATH, '//tr[2]/td[3]').text
                print("Tesla's most recent patent filing: {}".format(top_patent_title))

                link = driver.find_element(By.XPATH, '//tr[2]/td[3]')
                link.click()
                date_filed = driver.find_element(By.XPATH, '//table/tbody/tr[3]/td[2]/b').text
                abstract = driver.find_element(By.XPATH, '//body[@bgcolor="#FFFFFF"]/p[2]').text

                # on next page, to get to the date filed use xpath //tbody/tr[3]/td[2]/b

                patentEntry = {'patent': top_patent_title,
                               'filing date': date_filed,
                               'abstract': abstract,
                               'scraped_at': str(dateTimeObj)}

                with open('newpatent.json', 'w') as outfile:
                    json.dump(patentEntry, outfile)

            finally:
                driver.close()

    # except Exception as e:
    #     print("error occured")
checkPatent()
schedule.every().hour.do(checkPatent)
while True:
    # Checks whether a scheduled task
    # is pending to run or not
    schedule.run_pending()
    time.sleep(1)