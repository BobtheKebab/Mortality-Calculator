from django.shortcuts import render
from calculator.models import DataParser
import plotly.express as px

def index(request):
    return render(request, 'calculator/index.html')



def results(request):
    
    dp = DataParser()

    query_results = dp.getDeathCauses(request.GET['Sex'], request.GET['Ethnicity'], 5)
    results_df = query_results

    fig = px.bar(results_df, 
            x="age_adjusted_death_rate", 
            y="leading_cause", 
            orientation='h',
            labels=dict(age_adjusted_death_rate="Age Adjusted Death Rate per 100,000", 
            leading_cause="Top 5 Causes of Death"),
            color="leading_cause", 
            hover_data=["age_adjusted_death_rate"])

    # Hide legend
    fig.update_traces(showlegend=False)
    fig.update_layout(autosize=True)

    # Hide controls for chart
    config = dict({'displayModeBar': False})

    graph = fig.to_html(full_html=False, config=config)
    query_results = graph

    context = {'query_results': query_results}
    return render(request, 'calculator/results.html', context)



def visualize(request):

    dp = DataParser()
    query_results = dp.visualizeDeathCauses()

    df = query_results

    fig = px.bar(df, 
            x="leading_cause", 
            y="age_adjusted_death_rate", 
            color="race_ethnicity",
            barmode='group',
            labels=dict(age_adjusted_death_rate="Age Adjusted Death Rate per 100,000", 
            leading_cause="Cause of Death",
            ),
            hover_data=["age_adjusted_death_rate", "sex", "race_ethnicity", "year"], 
            facet_col="sex",
            animation_frame="year", 
            animation_group="leading_cause",
            range_y=[0,350])

    fig.update_layout(autosize=True, height=700)
    fig.update_layout(legend_title_text='Ethnicity')

    # Make animation bar appear lower to not conflict with labels
    fig['layout']['updatemenus'][0]['pad']=dict(r= 10, t= 150)
    fig['layout']['sliders'][0]['pad']=dict(r= 10, t= 150)

    # Update labels for male and female
    fig.for_each_annotation(lambda a: a.update(text=a.text.replace("sex=", "")))

    config = dict({'displayModeBar': True})
    graph = fig.to_html(full_html=False, config=config)
    query_results = graph

    context = {'query_results': query_results}
    return render(request, 'calculator/visualize.html', context)