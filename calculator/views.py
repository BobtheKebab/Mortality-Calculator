from django.shortcuts import render
from calculator.models import DataParser
import pandas as pd
import plotly.express as px
import plotly.offline as opy


def index(request):
    return render(request, 'calculator/index.html')

def results(request):
    dp = DataParser()
    query_results = dp.getDeathCauses(request.GET['Sex'], request.GET['Ethnicity'], 5)

    results_df = query_results
    results_df = results_df.astype({"age_adjusted_death_rate": float})
    results_df = results_df.sort_values(by=['age_adjusted_death_rate'], ascending=True)

    fig = px.bar(results_df, x="age_adjusted_death_rate", y="leading_cause", orientation='h',
    labels=dict(age_adjusted_death_rate="Age Adjusted Death Rate", leading_cause="Top 5 Causes of Death"))

    #placeholder labels
    #for idx in range(len(fig.data)):
        #fig.data[idx].y = ['1','2','3', '4', '5']


    graph = fig.to_html(full_html=False, default_height=700, default_width=1200)
    query_results = graph
    context = {'query_results': query_results}
    return render(request, 'calculator/results.html', context)

def visualize(request):
    dp = DataParser()
    query_results = dp.visualizeDeathCauses().to_html()
    context = {'query_results': query_results}
    return render(request, 'calculator/visualize.html', context)