from django.views.generic import TemplateView
from django.shortcuts import render
import json
import boto3
from teslaspectra import settings

#create  a connection to S3 using boto3 and the AWS access keys hidden in settings.py
s3 = boto3.client('s3', aws_access_key_id=settings.S3_access_key_id,
                  aws_secret_access_key=settings.S3_secret_access_key)


def homepage(request):
   #pricecheck s3 objects
    with open("selenium/json/modelSCurrentPrices.json", "wb") as readfile:
        s3.download_fileobj("teslaspectrajson", "modelSCurrentPrices.json", readfile)
    with open('selenium/json/modelSCurrentPrices.json', 'r') as f:
        #json.load provides us with a python dictionary from the json file
        prices = json.load(f)

    #patent details s3 object- Render the context as 'context_data' taking in the python dictionary as the key.
    with open("selenium/json/scrapedpatents.json", "wb") as f:
        s3.download_fileobj("teslaspectrajson", "scrapedpatents.json", f)

    with open('selenium/json/scrapedpatents.json', 'r') as patentdetails:
        newestPatentDetails = json.load(patentdetails)

    #tesla motors s3 object writing to the local json file as well as setting variable values.
    with open("selenium/json/rTeslaMotors.json", "wb") as f:
        s3.download_fileobj("teslaspectrajson", "rTeslaMotors.json", f)
    with open('selenium/json/rTeslaMotors.json', 'r') as redditpost:
        teslareddit = json.load(redditpost)

    with open('selenium/json/.json', 'wb') as f:
        s3.download_fileobj('teslaspectrajson', 'TheLimitingFactorS3.json', f)
    with open('selenium/json/TheLimitingFactor.json', 'r') as thelimitingfactor:
        thelimitingfactor = json.load(thelimitingfactor)

        return render(request, 'index.html', {'present_data': prices, 'recent_patent': newestPatentDetails,
                                              'rTeslaMotors': teslareddit})


def youtube_page(request):
    with open('selenium/json/youtubeinfo.json', 'wb') as f:
        s3.download_fileobj('teslaspectrajson', 'youtubeinfo.json', f)
    with open('selenium/json/youtubeinfo.json', 'r') as youtube_videos_stored:
        youtube_videos = json.load(youtube_videos_stored)
        channels = ["tesla_daily", "the_tesla_space", "the_limiting_factor"]

    return render(request, 'onyoutube.html', {'youtube_vids': youtube_videos, 'channels':channels
                                             })


class test_page(TemplateView):
    template_name ='test.html'

class youtube_page_class(TemplateView):
    template_name = 'onyoutube.html'

class thanks_page(TemplateView):
    template_name = 'thanks.html'


def model_s_prices(request):
    with open("selenium/json/modelSCurrentPrices.json", "wb") as f:
        s3.download_fileobj("teslaspectrajson", "modelSCurrentPrices.json", f)
    with open('selenium/json/modelSCurrentPrices.json', 'r') as f:
        #json.load provides us with a python dictionary from the json file
        prices = json.load(f)

    with open("selenium/json/modelSHistoricalPrices.json", "wb") as f:
        s3.download_fileobj("teslaspectrajson", "modelSHistoricalPrices.json", f)
    with open('selenium/json/modelSHistoricalPrices.json', 'r') as f2:
        pastPrices = json.load(f2)
#Render the context as 'context_data' taking in the python dictionaries as the key.
        return render(request, 'test.html', {'present_data': prices, 'past_data': pastPrices})

