from django.shortcuts import render
from calculator.models import DataParser

def index(request):
    return render(request, 'calculator/index.html')

def results(request):
    dp = DataParser()
    query_results = dp.getDeathCauses(request.GET['Sex'], request.GET['Ethnicity'], 5).to_html() # html table of results
    context = {'query_results': query_results}
    return render(request, 'calculator/results.html', context)