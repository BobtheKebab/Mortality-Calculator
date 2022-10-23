from django.shortcuts import render
from calculator.models import DataParser

def index(request):
    return render(request, 'calculator/index.html')

def results(request):
    print(request.GET['Sex'])
    dp = DataParser()
    query_results = dp.getDeathCauses("Male", "Non-Hispanic White", 5).to_html() # html table of results
    context = {'query_results': query_results}
    return render(request, 'calculator/results.html', context)