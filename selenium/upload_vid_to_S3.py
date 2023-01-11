import os
import json
import time
import boto3
import logging
from logs import secretkeys
#Convert relative to absolute paths to avoid conflict in crontab
script_path = os.path.abspath(__file__)  # i.e. /path/to/selenium/script.py
script_dir = os.path.split(script_path)[0]  #i.e. /path/to/selenium/

# create  a connection to S3 using boto3 and the AWS access keys hidden in settings.py
s3 = boto3.client('s3', aws_access_key_id=secretkeys.aws_access_key_id,
                  aws_secret_access_key=secretkeys.aws_secret_access_key)



# logging.basicConfig(filename='logs/youtube.log', filemode='w',
#                     format='%(asctime)s - %(message)s', level=logging.INFO)


def upload_vid_details_to_S3(videoDetails):
    with open(script_dir + '/json/youtubeinfo.json','w') as outfile:
        json.dump(videoDetails, outfile)
        # logging.info("local Json loaded with scrape")

    with open(script_dir + "/json/youtubeinfo.json", "rb") as f:
        s3.upload_fileobj(f, "teslaspectrajson", "youtubeinfo.json")
        # logging.info("video details uploaded to S3")
