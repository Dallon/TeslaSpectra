import logging
import os
import timeit
import requests
import json
import googleapiclient.errors
from logs import secretkeys
from store_youtube_video_info import store_video_details
from upload_vid_to_S3 import upload_vid_details_to_S3
from check_tag_compare_title_youtube import check_e_tag_compare_title
import googleapiclient.discovery
script_path = os.path.abspath(__file__)  # i.e. /path/to/whatever
script_dir = os.path.split(script_path)[0]  #i.e. /path/to/whatever
logging.basicConfig(filename='logs/youtube.log', filemode='w',
                    format='%(asctime)s - %(message)s', level=logging.INFO)


def youtubescrape():
    try:
        channels = [secretkeys.tesla_daily_id, secretkeys.the_limiting_factor_id,
                secretkeys.the_tesla_space_id]

        videoDetails = {}

        for channel in channels:
            new_scrape = False

            # the ID of the YouTube channel
            CHANNEL_TITLE = channel["channel_title"]
            CHANNEL_ID = channel["ID"]

            # Set the API key for the YouTube API
            API_KEY = secretkeys.youtube_api_key

            # Create a YouTube API service object
            youtube = googleapiclient.discovery.build('youtube', 'v3', developerKey=API_KEY)

            # Call the search.list method to search for videos within the specified channel
            request = youtube.search().list(
                part='id,snippet',
                channelId=CHANNEL_ID,
                type='video',
                order='date',
                maxResults=1
            )

            # Execute the request
            response = request.execute()

            # Get the e-tag from the response
            e_tag = response.get('ETag')
            for video in response['items']:
                title = video['snippet']['title']

            #compare the e_tag and title stored to the newly scraped respective values
            videoDetailsStored = check_e_tag_compare_title(CHANNEL_TITLE, e_tag, title)
            # print(videoDetailsStored)

            logging.info("videoDetailStored Function completed for {}".format(CHANNEL_TITLE))
            # if the video details are already stored, add the previously scraped details to
            # VideoDetails using stored_video_details function
            if videoDetailsStored:
                logging.info("videoDetails already stored for {}".format(CHANNEL_TITLE))
                with open(script_dir + "/json/youtubeinfo.json", "rb") as f:
                    storedDetails = json.load(f)
                #title already declared above
                description = storedDetails["{} description".format(CHANNEL_TITLE)]
                embed_url = storedDetails["{} embed_url".format(CHANNEL_TITLE)]
                published_at = storedDetails["{} published_at".format(CHANNEL_TITLE)]
                e_tag = e_tag
                store_video_details(videoDetails, title, description,
                                    embed_url, published_at, e_tag, CHANNEL_TITLE)

            if not videoDetailsStored:
                new_scrape = True
                logging.info("the video details have not been scraped for {}".format(CHANNEL_TITLE))
                # Iterate over the list of videos
                for video in response['items']:
                    # Extract the video ID, title, description, published date, embed_url
                    videoId = video['id']['videoId']
                    title = video['snippet']['title']
                    description = video['snippet']['description']
                    published_at = video['snippet']['publishedAt']

                    # Build the video embed URL
                    embed_url = f'https://www.youtube.com/embed/{videoId}'

                    #attach video details to the dictionary
                    store_video_details(videoDetails, title, description,
                                                embed_url, published_at, e_tag, CHANNEL_TITLE)
                    logging.info("video details added to dictionary for {}".format(CHANNEL_TITLE))

    except Exception as e:
        logging.info(e)
    except googleapiclient.errors as error:
        logging.info(f'An error occurred: {error}')

    finally:
        if new_scrape:
            upload_vid_details_to_S3(videoDetails)
            # print("end of script--------------------------------------------------------------------")
            logging.info("uploaded details, end of script-------------------------------------------------------------")
        else:
            logging.info("not uploading details, script ended")


youtubescrape()
# print(timeit.Timer(youtubescrape).timeit(number=1))