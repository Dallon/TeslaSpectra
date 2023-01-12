from django.views.generic import TemplateView
from django.shortcuts import render, redirect
import json
import boto3
from teslaspectra import settings

#create  a connection to S3 using boto3 and the AWS access keys hidden in settings.py
s3 = boto3.client('s3', aws_access_key_id=settings.S3_access_key_id,
                  aws_secret_access_key=settings.S3_secret_access_key)


def homepage(request):
   #pricecheck s3 objects
    with open("scrapers/json/modelSCurrentPrices.json", "wb") as readfile:
        s3.download_fileobj("teslaspectrajson", "modelSCurrentPrices.json", readfile)
    with open('scrapers/json/modelSCurrentPrices.json', 'r') as f:
        #json.load provides us with a python dictionary from the json file
        prices = json.load(f)

    #patent details s3 object- Render the context as 'context_data' taking in the python dictionary as the key.
    with open("scrapers/json/scrapedpatents.json", "wb") as f:
        s3.download_fileobj("teslaspectrajson", "scrapedpatents.json", f)

    with open('scrapers/json/scrapedpatents.json', 'r') as patentdetails:
        newestPatentDetails = json.load(patentdetails)

    return render(request, 'index.html', {'present_data': prices,
                                              'recent_patent': newestPatentDetails
                                              })


def youtube_page(request):
    with open('scrapers/json/youtubeinfo.json', 'wb') as f:
        s3.download_fileobj('teslaspectrajson', 'youtubeinfo.json', f)
    with open('scrapers/json/youtubeinfo.json', 'r') as youtube_videos_stored:
        youtube_videos = json.load(youtube_videos_stored)
        channels = ["Tesla Daily", "The Tesla Space", "The Limiting Factor"]


    return render(request, 'onyoutube.html', {'youtube_vids': youtube_videos, 'channels':channels
                                             })


def reddit_page(request):
    with open('scrapers/json/subreddits.json', 'wb') as f:
        s3.download_fileobj('teslaspectrajson', 'subreddits.json', f)
    with open('scrapers/json/subreddits.json', 'r') as subreddit_details:
        subreddit_details = json.load(subreddit_details)
        subreddits = ["TeslaMotors", "TeslaInvestorsClub", "Cybertruck", "RealTesla",
                      "TeslaPorn"]

    return render(request, 'onreddit.html', {'subreddit_details': subreddit_details, 'subreddits':subreddits
                                             })




class test_page(TemplateView):
    template_name ='test.html'

class youtube_page_class(TemplateView):
    template_name = 'onyoutube.html'

class thanks_page(TemplateView):
    template_name = 'thanks.html'

class reddit_page_class(TemplateView):
    template_name = 'onreddit.html'


def model_s_prices(request):
    with open("scrapers/json/modelSCurrentPrices.json", "wb") as f:
        s3.download_fileobj("teslaspectrajson", "modelSCurrentPrices.json", f)
    with open('scrapers/json/modelSCurrentPrices.json', 'r') as f:
        #json.load provides us with a python dictionary from the json file
        prices = json.load(f)

    with open("scrapers/json/modelSHistoricalPrices.json", "wb") as f:
        s3.download_fileobj("teslaspectrajson", "modelSHistoricalPrices.json", f)
    with open('scrapers/json/modelSHistoricalPrices.json', 'r') as f2:
        pastPrices = json.load(f2)
#Render the context as 'context_data' taking in the python dictionaries as the key.
        return render(request, 'test.html', {'present_data': prices, 'past_data': pastPrices})

