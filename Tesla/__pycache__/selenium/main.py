from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from datetime import datetime
import time
import os
import json

website = 'https://www.tesla.com/models/design#overview'
s = Service('/Users/Compuester/Documents/chromedriver')

dateTimeObj = datetime.now()
Model_S_Price = {}
date_format = '%Y-%m-%d %H:%M:%S.%f'


def price_update():

    driver = webdriver.Chrome(service=s)
    try:
        driver.get(website)
        time.sleep(3)
        ModelS = driver.find_element\
            (By.XPATH,"//div[@id='root']//label[contains(@for, '$MTS12-Model')]//p[contains(@class, 'price-not-included')]").text
        ModelSPlaid = driver.find_element\
            (By.XPATH, "//div[@id='root']//label[contains(@for, '$MTS11-Model')]//p[contains(@class, 'price-not-included')]").text

        #below we remove the commas and dollar signs from the Car model prices so we can later compare
        # the integer values to historical prices.

        ModelS = ModelS.replace("$", "").replace(",", "")
        ModelSPlaid = ModelSPlaid.replace("$", "").replace(",", "")
        prices = {'Model_S': ModelS,
                  'Model_S_Plaid': ModelSPlaid,
                  'scraped_at': str(dateTimeObj)}
        print(prices)


        #Below we first check if the file is empty

        filepath = 'modelSHistoricalPrices.json'
        if os.stat(filepath).st_size == 0:
            data = [prices]

            with open('modelSHistoricalPrices.json', 'w') as outfile:
                json.dump(data, outfile)

        # we now need to compare the new scraped values with the values from modelSHistoricalPrices.json.
        # 1st we open the json file in read mode and then compare the latest price in HistoricalPrices
        # (sorted by date) with the newly scraped value. If the values are equal
        # we don't do anything with the scraped data. If the values are different
        # we append the scraped data to the assigned variable and overwrite the json file contents.
        else:
            print("checking data in the historical prices file.... Loading file")

            with open("modelSHistoricalPrices.json", "r") as read_content:
                # here we convert the json object in the file into a python dict. These dicts
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
                pass
            else:
                print("prices have changed--- logging changes")
                with open("modelSCurrentPrices.json", "w") as outfile:
                    json.dump(prices, outfile)
                    print("current price json updated")

                sorted_dicts.append(prices)
                print(sorted_dicts)
                with open("modelSHistoricalPrices.json", "w") as outfile:
                    json.dump(sorted_dicts, outfile)
                    print("historical prices json updated")

    except Exception as e:
        print(e)

    finally:
        driver.close() #refers to the connection to the selenium driver


price_update()

