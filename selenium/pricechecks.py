from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from datetime import datetime
import os
import time
import json
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import boto3
from logs import secretkeys

"""Convert relative to absolute paths to avoid conflict in crontab"""
script_path = os.path.abspath(__file__) # i.e. /path/to/selenium/script.py
script_dir = os.path.split(script_path)[0] #i.e. /path/to/selenium/

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
dateTimeObj = datetime.now()
website = 'https://www.tesla.com/en_CA/models/design?redirect=no#overview'
s = Service(ChromeDriverManager().install())

Model_S_Price = {}
date_format = '%Y-%m-%d %H:%M:%S.%f'


#create  a connection to S3 using boto3 and the AWS access keys hidden in settings.py
s3 = boto3.client('s3', aws_access_key_id=secretkeys.aws_access_key_id,
                  aws_secret_access_key=secretkeys.aws_secret_access_key)


def price_update():
    driver = webdriver.Chrome(service=s, options=chrome_options)
    try:
        driver.get(website)
        time.sleep(3)
        element = driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div[1]/dialog/div/button")
        element.click()
        time.sleep(1)
        ModelS = driver.find_element(By.XPATH, "//div[@id='root']"
                                    "//label[contains(@for, '$MTS13-Model')]//span[3]//p").text

        ModelSPlaid = driver.find_element(By.XPATH, "//div[@id='root']"
                                    "//label[contains(@for, '$MTS14-Model')]//span[3]//p").text

        # below we remove the commas and dollar signs from the Car model prices so we can later compare
        # the integer values to historical prices.

        ModelS = ModelS.replace("$", "").replace(",", "")
        ModelSPlaid = ModelSPlaid.replace("$", "").replace(",", "")
        prices = {'Model_S': ModelS,
                  'Model_S_Plaid': ModelSPlaid,
                  'scraped_at': str(dateTimeObj)}
        # print("the scraped prices are {}".format(prices))

        # Below we first check if the file is empty
        filepath = script_dir + '/json/modelSHistoricalPrices.json'
        if os.stat(filepath).st_size == 0:
            data = [prices]

            with open(script_dir + '/json/modelSHistoricalPrices.json', 'w') as outfile:
                json.dump(data, outfile)

        # we now need to compare the new scraped values with the values from modelSHistoricalPrices.json.
        #  1st we open the json file in read mode and then compare the latest price in HistoricalPrices
        #  (sorted by date) with the newly scraped value. If the values are equal
        #  we don't do anything with the scraped data. If the values are different
        #  we append the scraped data to the assigned variable and overwrite the json file contents.
        else:
            # print("checking data in the historical prices file.... Loading file")

            with open(script_dir + "/json/modelSHistoricalPrices.json", "r") as read_content:
                # here we convert the json object in the file into a python dict. These dictionaries
                # are in a list.[{}]
                unsorted_dicts = json.load(read_content)

            # We sort the dictionaries within the lists using an anonymous function(lamdba) to sort
            # them by the parameter "scraped_at" using datetime.strptime
            sorted_dicts = sorted(unsorted_dicts,
                                  key=lambda x: datetime.strptime(x["scraped_at"], date_format))

            # and here we assign variables to the scraped prices of the Model_S and Plaid cars.
            histPriceModelS = sorted_dicts[-1]['Model_S']
            histPriceModelSPlaid = sorted_dicts[-1]['Model_S_Plaid']

            if ModelS == histPriceModelS and ModelSPlaid == histPriceModelSPlaid:
                print("prices haven't changed")
                pass
            else:
                print("prices have changed--- logging changes")
                with open(script_dir + "/json/modelSCurrentPrices.json", "w") as outfile:
                    json.dump(prices, outfile)
                    print("current price json updated")

                with open(script_dir + '/json/modelSCurrentPrices.json', 'rb') as f:
                    s3.upload_fileobj(f, "teslaspectrajson", "modelSCurrentPrices.json")

                sorted_dicts.append(prices)
                # print(sorted_dicts)
                with open(script_dir + "/json/modelSHistoricalPrices.json", "w") as outfile:
                    json.dump(sorted_dicts, outfile)

                with open(script_dir + '/json/modelSHistoricalPrices.json', 'rb') as f:
                    s3.upload_fileobj(f, "teslaspectrajson", "modelSHistoricalPrices.json")
                    print("historical prices json updated")

    except Exception as e:
        print(e)

    finally:
        driver.quit()  # refers to the connection to the selenium driver
        print("driver.quit")


price_update()
