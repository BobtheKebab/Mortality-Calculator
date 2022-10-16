from django.http import HttpResponse
from django.template import loader

def index(request):
    template = loader.get_template('calculator/index.html')
    return HttpResponse(template.render())

def results(request):
    template = loader.get_template('calculator/results.html')
    return HttpResponse(template.render())