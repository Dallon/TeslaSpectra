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
s3 = boto3.client('s3', aws_access_key_id=secretkeys.aws_access_key_id,
                  aws_secret_access_key=secretkeys.aws_secret_access_key)
"""Convert relative to absolute paths to avoid conflict in crontab"""
script_path = os.path.abspath(__file__)  # i.e. /path/to/selenium/script.py
script_dir = os.path.split(script_path)[0]  #i.e. /path/to/selenium/
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
dateTimeObj = datetime.now()
website = 'https://www.youtube.com/channel/UCIFn7ONIJHyC-lMnb7Fm_jw'
s = Service(ChromeDriverManager().install())
date_format = '%Y-%m-%d %H:%M:%S.%f'


def LimitingFactorScrape():

    driver = webdriver.Chrome(service=s, options=chrome_options)
    try:
        driver.get(website)
        driver.implicitly_wait(4)
        videoTitle = driver.find_element(By.XPATH, "//div[@class='style-scope ytd-grid-video-renderer']//a[@id='video-title'][1]").text
        videoLink = driver.find_element(By.XPATH, "//div[@class='style-scope ytd-grid-video-renderer']//a[@id='video-title'][1]").get_attribute("href")
        videoClickableLink = driver.find_element(By.XPATH, "//div[@class='style-scope ytd-grid-video-renderer']//a[@id='video-title'][1]")
        videoViews = driver.find_element(By.XPATH, "//span[@class='style-scope ytd-grid-video-renderer'][1]").text
        videoPostDate = driver.find_element(By.XPATH, "//span[@class='style-scope ytd-grid-video-renderer'][1]/following-sibling::span").text
        videoClickableLink.click()
        shareButton = driver.find_element(By.XPATH, "//ytd-button-renderer[contains(@class, 'force-icon-button')]//button[@aria-label='Share'][1]")
        shareButton.click()
        embedButton = driver.find_element(By.XPATH, "//button[@title='Embed']")
        embedButton.click()
        # startVideoAtZero = driver.find_element(By.XPATH, "//div[@id='start-at-wrapper']//paper-ripple/preceding-sibling::div")
        #
        # startVideoAtZero.click()
        embedCode = driver.find_element(By.XPATH, "//tp-yt-iron-autogrow-textarea").get_attribute("value")
        embedCode = embedCode.replace('\"', "")
        embedCode =embedCode[7:-10]
        
        print(videoTitle, " ", videoViews, " ", videoPostDate)

        videoDetails = {
            'videoTitle': videoTitle,
            'videoLink': videoLink,
            'videoViews':videoViews,
            'videoPostDate': videoPostDate,
            'embedCode':embedCode
        }


        limitingFactorScrape = script_dir + '/json/TheLimitingFactor.json'
        if os.stat(limitingFactorScrape).st_size == 0:
            with open(script_dir + '/json/TheLimitingFactor.json','w') as outfile:
                json.dump(videoDetails, outfile)
                print("Json file was Empty- now loaded with most recent scrape")

            with open(script_dir + "/json/TheLimitingFactor.json", "rb") as f:
                s3.upload_fileobj(f, "teslaspectrajson", "TheLimitingFactorS3.json")
                print("video uploaded to S3")
        else:
            with open(script_dir + '/json/TheLimitingFactor.json', 'r') as readfile:
                archivedScrape = json.load(readfile)
                print(archivedScrape)

            if archivedScrape['videoTitle'] == videoDetails['videoTitle']:
                print("no new video posted")
                with open(script_dir + '/json/TheLimitingFactor.json', 'w') as outfile:
                    json.dump(videoDetails, outfile)

                with open(script_dir + "/json/TheLimitingFactor.json", "rb") as f:
                    s3.upload_fileobj(f, "teslaspectrajson", "TheLimitingFactorS3.json")
                    print("video views/date updated in S3")

            else:
                with open(script_dir + '/json/TheLimitingFactor.json', 'w') as outfile:
                    json.dump(videoDetails, outfile)


                with open(script_dir + "/json/TheLimitingFactor.json", "rb") as f:
                    s3.upload_fileobj(f, "teslaspectrajson", "TheLimitingFactorS3.json")
                    print("a new video was posted--new video details uploaded to S3")
    except Exception as e:
        print(e)

    finally:
        driver.quit()
        print("driver quit")

LimitingFactorScrape()