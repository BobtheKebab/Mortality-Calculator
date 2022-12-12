from django.shortcuts import render
from calculator.models import DataParser
import plotly.express as px

Y_AXIS_MOD = 0.05; # Multiplier to be used when calculating y-axis range


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
    uniqueCauses = df["leading_cause"].unique() # Will be used for form dropdown

    # Determine y-axis range by rounding  max value from dataframe and adding constant
    yAxis = df['age_adjusted_death_rate'].max()
    yAxis = round(yAxis, -1)
    yAxis = yAxis + round(yAxis * Y_AXIS_MOD, -1)

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
            range_y=[0,yAxis])

    fig.update_layout(autosize=True, height=600)
    fig.update_layout(legend_title_text='Ethnicity')

    # Make animation bar appear lower to not conflict with labels
    fig['layout']['updatemenus'][0]['pad']=dict(r= 10, t= 150)
    fig['layout']['sliders'][0]['pad']=dict(r= 10, t= 150)

    # Update labels for male and female
    fig.for_each_annotation(lambda a: a.update(text=a.text.replace("sex=", "")))

    config = dict({'displayModeBar': True})
    graph = fig.to_html(full_html=False, config=config)
    query_results = graph

    context = {'query_results': query_results, 'uniqueCauses': uniqueCauses}
    return render(request, 'calculator/visualize.html', context)



def compareForm(request):
    dp = DataParser()
    query_results = dp.visualizeDeathCauses()
    uniqueCauses = query_results["leading_cause"].unique() # Will be used for form dropdown

    context = {'uniqueCauses': uniqueCauses}
    return render(request, 'calculator/compareForm.html', context)



def compare(request):
    
    # Getting variables from form
    sex1 = request.GET['sex1']
    ethnicity1 = request.GET['ethnicity1']
    cause1 = request.GET['cause1']

    sex2 = request.GET['sex2']
    ethnicity2 = request.GET['ethnicity2']
    cause2 = request.GET['cause2']

    # List to show if inputted sex, ethnicity, and cause (respectively) are the same
    # 1 for same, 0 for not
    similarity = [0, 0, 0]
    similarity[0] = sex1 == sex2
    similarity[1] = ethnicity1 == ethnicity2
    similarity[2] = cause1 == cause2

    dp = DataParser()
    query_results = dp.compareDeathCauses()
    df = query_results

    data = df[((df.sex == sex1) & (df.race_ethnicity == ethnicity1) & (df.leading_cause == cause1))
         | ((df.sex == sex2) & (df.race_ethnicity == ethnicity2) & (df.leading_cause == cause2))]

    # color input for graph
    clr = "race_ethnicity"
    # title for legend
    title = "Ethnicity"
    # Determine y-axis range by rounding  max value from dataframe and adding const
    yAxis = data['age_adjusted_death_rate'].max()
    yAxis = round(yAxis, -1)
    yAxis = yAxis + round(yAxis * Y_AXIS_MOD, -1)

    if ( similarity == [0, 1, 0] ):
        clr = "sex"
        title = "Sex"
    if ( similarity == [1, 1, 0] ):
        clr = "leading_cause"
        title = "Cause of Death"

    if ( similarity == [0, 1, 1] ):
        fig = px.bar(data, 
            x="leading_cause", 
            y="age_adjusted_death_rate", 
            color="sex",
            labels=dict(age_adjusted_death_rate="Age Adjusted Death Rate per 100,000", 
            leading_cause="Cause of Death",
            ),
            hover_data=["age_adjusted_death_rate", "sex", "race_ethnicity", "year"], 
            facet_col="sex",
            animation_frame="year", 
            animation_group="leading_cause",
            range_y=[0,yAxis])
        # Remove sex labels on top of each facet
        fig.for_each_annotation(lambda a: a.update(text=a.text.replace("sex=Male", "")))
        fig.for_each_annotation(lambda a: a.update(text=a.text.replace("sex=Female", "")))
        # Change legend title
        fig.update_layout(legend_title_text='Sex')
    else:
        fig = px.bar(data, 
            x="leading_cause", 
            y="age_adjusted_death_rate", 
            color=clr,
            labels=dict(age_adjusted_death_rate="Age Adjusted Death Rate per 100,000", 
            leading_cause="Cause of Death",
            ),
            hover_data=["age_adjusted_death_rate", "sex", "race_ethnicity", "year"], 
            animation_frame="year", 
            animation_group="leading_cause",
            range_y=[0,yAxis])
        fig.update_layout(legend_title_text=title)

    if ( (similarity == [0, 0, 1]) | (similarity == [1, 0, 1]) ):
        fig.update_layout(barmode="group")

    fig.update_layout(autosize=True, height=600)

    config = dict({'displayModeBar': False}) # Hide graph controls
    graph = fig.to_html(full_html=False, config=config)

    context = {'graph': graph}

    return render(request, 'calculator/compare.html', context)



def compareCity(request):

    dp = DataParser()
    data = dp.prepCSV()

    # Determine y-axis range by rounding  max value from dataframe and adding const
    yAxis = data['age_adjusted_death_rate'].max()
    yAxis = round(yAxis, -1)
    yAxis = yAxis + round(yAxis * Y_AXIS_MOD, -1)

    fig = px.bar(data, 
            x="leading_cause", 
            y="age_adjusted_death_rate", 
            color="city",
            labels=dict(age_adjusted_death_rate="Age Adjusted Death Rate per 100,000", 
            leading_cause="Cause of Death",
            city = "City"
            ), 
            facet_col="sex",
            animation_frame="year", 
            animation_group="leading_cause", 
            range_y=[0,yAxis], 
            barmode="group")

    fig.update_layout(autosize=True, height=600)

    # Make animation bar appear lower to not conflict with labels
    fig['layout']['updatemenus'][0]['pad']=dict(r= 10, t= 150)
    fig['layout']['sliders'][0]['pad']=dict(r= 10, t= 150)

    # Update labels for male and female
    fig.for_each_annotation(lambda a: a.update(text=a.text.replace("sex=", "")))
    fig.for_each_annotation(lambda a: a.update(text=a.text.replace("oslo", "Oslo")))

    graph = fig.to_html(full_html=False)
    context = {'graph': graph}

    return render(request, 'calculator/compareCity.html', context)