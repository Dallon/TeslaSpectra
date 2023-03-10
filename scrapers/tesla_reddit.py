import json
from datetime import datetime, timedelta
from logs import secretkeys
import praw
import boto3
import os
import timeit
# import timeit
import logging
#Convert relative to absolute paths to avoid conflict in crontab
script_path = os.path.abspath(__file__) # i.e. /path/to/selenium/script.py
script_dir = os.path.split(script_path)[0] #i.e. /path/to/selenium/

#create  a connection to S3 using boto3 and the AWS access keys hidden in settings.py
s3 = boto3.client('s3', aws_access_key_id=secretkeys.aws_access_key_id,
                  aws_secret_access_key=secretkeys.aws_secret_access_key)

dateTimeObj = datetime.now()
logging.basicConfig(filename='logs/tesla_reddit.log', filemode='w',
                    format='%(asctime)s - %(message)s', level=logging.INFO)


#this function relies on the RedditAPI, and is in compliance with their scraping standards
def retrieve_post_details():
    try:
        CLIENT_ID = secretkeys.reddit_api_client_id
        SECRET_KEY = secretkeys.reddit_api_secret_key
        reddit_read_only = praw.Reddit(client_id=CLIENT_ID,

                             client_secret=SECRET_KEY,

                             redirect_uri='http://localhost:8080',

                             user_agent='TeslaSpectra by /u/RepulsivePromotion58',
                             )
        subreddits = ["TeslaMotors", "TeslaInvestorsClub","Cybertruck","RealTesla"]
        topPostDict = {}
        for subreddit in subreddits:
            subreddit = reddit_read_only.subreddit(subreddit)
            topPostOfDay = False
            for post in subreddit.hot(limit=4):
                #post.created is the utc timestamp
                created_utc = post.created
                #we use .date() at the end below to convert from datetime.datetime to datetime.date
                #so we can compare today's date with the post date.
                postDate = datetime.utcfromtimestamp(created_utc).date()
                #today's date
                todaysDate = datetime.today().date()
                timeSincePost = todaysDate - postDate
                postTitle = post.title


                # print(timedelta(days=1))
                if timeSincePost > timedelta(days=2) or "thread" in postTitle.lower():
                    continue
                if topPostOfDay:
                    break

                else:
                    topPostOfDay = True
                    postUpvotes = post.score
                    postTitle = post.title
                    postUrl = post.permalink

                    if int(postUpvotes) <= 1000:

                       hotPost = ""

                    else:
                        hotPost = "Hot"
                        print(hotPost)

                    topPostDict["{} postTitle".format(subreddit)] = postTitle
                    topPostDict["{} postUpvotes".format(subreddit)] = postUpvotes
                    topPostDict["{} hotPost".format(subreddit)] = hotPost
                    topPostDict["{} scraped_at".format(subreddit)] = str(dateTimeObj)
                    topPostDict["{} postLink".format(subreddit)] ="https://www.reddit.com/"+\
                                                                 postUrl
                    # print(topPostDict)
                    # print("{} postTitle".format(subreddit) +
                    #       " scraped")
                    logging.info("{} postTitle".format(subreddit) + "scraped")

        with open(script_dir + '/json/subreddits.json', 'w') as outfile:
            json.dump(topPostDict, outfile)

        logging.info("subreddits local JSON populated")

        with open(script_dir + "/json/subreddits.json", "rb") as f:
            s3.upload_fileobj(f, "teslaspectrajson", "subreddits.json")
        logging.info("subreddits S3 JSON populated")

    except Exception as e:
        logging.exception(e)

    finally:
        # print("all subreddits scraped")

        logging.info("scraper completed")


retrieve_post_details()


# print(timeit.Timer(retrieve_post_details).timeit(number=1))