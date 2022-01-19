from django.views.generic import TemplateView
from django.template.defaulttags import register
from django.shortcuts import render
import json


def HomePage(request):
    with open('/home/bitnami/htdocs/projects/TeslaSpectra/selenium/modelSCurrentPrices.json', 'r') as f:
        #json.load provides us with a python dictionary from the json file
        prices = json.load(f)
#Render the context as 'context_data' taking in the python dictionary as the key.
        return render(request,'index.html', {'present_data': prices})


class TestPage(TemplateView):
    template_name ='test.html'


class ThanksPage(TemplateView):
    template_name = 'thanks.html'


def modelSPrices(request):
    with open('/home/bitnami/htdocs/projects/TeslaSpectra/selenium/modelSCurrentPrices.json', 'r') as f:
        #json.load provides us with a python dictionary from the json file
        prices = json.load(f)

    with open('/home/bitnami/htdocs/projects/TeslaSpectra/selenium/modelSHistoricalPrices.json', 'r') as f2:
        pastPrices = json.load(f2)
#Render the context as 'context_data' taking in the python dictionaries as the key.
        return render(request, 'test.html',{'present_data': prices, 'past_data': pastPrices})
