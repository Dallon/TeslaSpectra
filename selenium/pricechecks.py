from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from datetime import datetime
import time
import os
import json
import logging
"""Convert relative to absolute paths to avoid conflict in crontab"""
script_path = os.path.abspath(__file__) # i.e. /path/to/selenium/script.py
script_dir = os.path.split(script_path)[0] #i.e. /path/to/selenium/

logging.basicConfig(format="%(name)s - %(levelname)s - %(message)s",
                    filename=script_dir + '/logs/pricechecks.log', level=logging.INFO)
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import boto3
from Tesla import settings


chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
dateTimeObj = datetime.now()
website = 'https://www.tesla.com/en_CA/models/design?redirect=no#overview'
s = Service(ChromeDriverManager().install())

Model_S_Price = {}
date_format = '%Y-%m-%d %H:%M:%S.%f'


#create  a connection to S3 using boto3 and the AWS access keys hidden in settings.py
s3 = boto3.client('s3', aws_access_key_id = settings.aws_access_key_id,
                  aws_secret_access_key= settings.aws_secret_access_key)

def price_update():
    driver = webdriver.Chrome(options=chrome_options)
    try:
        driver.get(website)
        time.sleep(3)
        logging.info("process started-------------------------------------------------------------")
        ModelS = driver.find_element(By.XPATH, "//div[@id='root']//label[contains(@for, '$MTS12-Model')]//"
                                               "p[contains(@class, 'price-not-included')]").text
        ModelSPlaid = driver.find_element(By.XPATH, "//div[@id='root']//label[contains(@for, '$MTS11-Model')]//"
                                                    "p[contains(@class, 'price-not-included')]").text

        # below we remove the commas and dollar signs from the Car model prices so we can later compare
        # the integer values to historical prices.

        ModelS = ModelS.replace("$", "").replace(",", "")
        ModelSPlaid = ModelSPlaid.replace("$", "").replace(",", "")
        prices = {'Model_S': ModelS,
                  'Model_S_Plaid': ModelSPlaid,
                  'scraped_at': str(dateTimeObj)}
        print("the scraped prices are {}".format(prices))
        logging.info("the scraped prices are {}".format(prices))

        # Below we first check if the file is empty
        filepath = script_dir + '/json/modelSHistoricalPrices.json'
        if os.stat(filepath).st_size == 0:
            data = [prices]
            logging.warning("had to populate the file with new data")

            with open(script_dir + '/json/modelSHistoricalPrices.json', 'w') as outfile:
                json.dump(data, outfile)

        # we now need to compare the new scraped values with the values from modelSHistoricalPrices.json.
        #  1st we open the json file in read mode and then compare the latest price in HistoricalPrices
        #  (sorted by date) with the newly scraped value. If the values are equal
        #  we don't do anything with the scraped data. If the values are different
        #  we append the scraped data to the assigned variable and overwrite the json file contents.
        else:
            print("checking data in the historical prices file.... Loading file")
            logging.info("checking data in the historical prices file.... Loading file")

            with open(script_dir + "/json/modelSHistoricalPrices.json", "r") as read_content:
                # here we convert the json object in the file into a python dict. These dictionaries
                # are in a list.[{}]
                unsorted_dicts = json.load(read_content)

            # We sort the dictionaries within the lists using an anonymous function(lamdba) to sort
            # them by the parameter "scraped_at" using datetime.strptime
            sorted_dicts = sorted(unsorted_dicts,
                                  key=lambda x: datetime.strptime(x["scraped_at"], date_format))
            print(sorted_dicts)

            # and here we assign variables to the scraped prices of the Model_S and Plaid cars.
            histPriceModelS = sorted_dicts[-1]['Model_S']
            histPriceModelSPlaid = sorted_dicts[-1]['Model_S_Plaid']

            if ModelS == histPriceModelS and ModelSPlaid == histPriceModelSPlaid:
                print("prices haven't changed")
                logging.info("prices haven't changed")
                pass
            else:
                print("prices have changed--- logging changes")
                with open(script_dir + "/json/modelSCurrentPrices.json", "w") as outfile:
                    json.dump(prices, outfile)
                    print("current price json updated")
                    logging.info("current price json updated")

                with open(script_dir + '/json/modelSCurrentPrices.json', 'rb') as f:
                    s3.upload_fileobj(f, "teslaspectrajson", "modelSCurrentPrices.json")


                sorted_dicts.append(prices)
                print(sorted_dicts)
                with open(script_dir + "/json/modelSHistoricalPrices.json", "w") as outfile:
                    json.dump(sorted_dicts, outfile)

                with open(script_dir + '/json/modelSHistoricalPrices.json', 'rb') as f:
                    s3.upload_fileobj(f, "teslaspectrajson", "modelSHistoricalPrices.json")
                    print("historical prices json updated")
                    logging.info("historical prices json updated")

    except Exception as e:
        print(e)
        logging.exception(e)

    finally:
        driver.close()  # refers to the connection to the selenium driver
        logging.info("program completed-------------------------------------------------------")


price_update()
