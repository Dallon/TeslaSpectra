from django.views.generic import TemplateView
from django.shortcuts import render
import json
import boto3
from teslaspectra import settings

#create  a connection to S3 using boto3 and the AWS access keys hidden in settings.py
s3 = boto3.client('s3', aws_access_key_id=settings.S3_access_key_id,
                  aws_secret_access_key=settings.S3_secret_access_key)


def HomePage(request):
    # create  a connection to S3 using boto3 and the AWS access keys hidden in settings.py
    s3 = boto3.client('s3', aws_access_key_id=settings.S3_access_key_id,
                      aws_secret_access_key=settings.S3_secret_access_key)
    with open("selenium/json/modelSCurrentPrices.json", "wb") as readfile:
        s3.download_fileobj("teslaspectrajson", "modelSCurrentPrices.json", readfile)
    with open('selenium/json/modelSCurrentPrices.json', 'r') as f:
        #json.load provides us with a python dictionary from the json file
        prices = json.load(f)

        #Render the context as 'context_data' taking in the python dictionary as the key.
    with open("selenium/json/scrapedpatents.json", "wb") as f:
        s3.download_fileobj("teslaspectrajson", "scrapedpatents.json", f)
    with open('selenium/json/scrapedpatents.json', 'r') as patentdetails:
        newestPatentDetails = json.load(patentdetails)
        #tesla motors s3 object writing to the local json file as well as setting variable values.
    with open("selenium/json/rTeslaMotors.json", "wb") as f:
        s3.download_fileobj("teslaspectrajson", "rTeslaMotors.json", f)
    with open('selenium/json/rTeslaMotors.json', 'r') as redditpost:
        teslareddit = json.load(redditpost)

    with open('selenium/json/TheLimitingFactor.json', 'wb') as f:
        s3.download_fileobj('teslaspectrajson', 'TheLimitingFactorS3.json', f)
    with open('selenium/json/TheLimitingFactor.json', 'r') as thelimitingfactor:
        thelimitingfactor = json.load(thelimitingfactor)

        return render(request, 'index.html', {'present_data': prices, 'recentPatent': newestPatentDetails,
                                              'rTeslaMotors': teslareddit, 'thelimitingfactor': thelimitingfactor})


class TestPage(TemplateView):
    template_name ='test.html'


class ThanksPage(TemplateView):
    template_name = 'thanks.html'


def modelSPrices(request):
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

