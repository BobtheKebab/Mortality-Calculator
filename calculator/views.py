from django.shortcuts import render
from calculator.models import DataParser
import plotly.express as px

def index(request):
    return render(request, 'calculator/index.html')

def results(request):
    dp = DataParser()
    query_results = dp.getDeathCauses(request.GET['Sex'], request.GET['Ethnicity'], 5)

    results_df = query_results
    results_df = results_df.astype({"age_adjusted_death_rate": float})
    results_df = results_df.sort_values(by=['age_adjusted_death_rate'], ascending=False)

    fig = px.bar(results_df, x="age_adjusted_death_rate", y="leading_cause", orientation='h',
    labels=dict(age_adjusted_death_rate="Age Adjusted Death Rate per 100,000", leading_cause="Top 5 Causes of Death"),
    color="leading_cause", hover_data=["age_adjusted_death_rate"])

    # Hide legend
    fig.update_traces(showlegend=False)
    fig.update_layout(autosize=True)

    # Hide controls for chart
    config = dict({'displayModeBar': False})

    #placeholder labels
    #for idx in range(len(fig.data)):
        #fig.data[idx].y = ['1','2','3', '4', '5']


    graph = fig.to_html(full_html=False, config=config)
    query_results = graph
    context = {'query_results': query_results}
    return render(request, 'calculator/results.html', context)

def visualize(request):
    dp = DataParser()
    query_results = dp.visualizeDeathCauses().to_html()
    context = {'query_results': query_results}
    return render(request, 'calculator/visualize.html', context)