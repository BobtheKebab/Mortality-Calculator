from django.shortcuts import render
from calculator.models import DataParser
import plotly.express as px

Y_AXIS_MOD = 0.05 # Multiplier to be used when calculating y-axis range
CHART_HEIGHT = 600 # Default chart height

# Landing page
def index(request):
    return render(request, 'calculator/index.html')



# Top 5 causes of death page
def results(request):
    
    # Initialize data parser model
    dp = DataParser()

    # Get causes for specified sex and ethnicity, put in dataframe
    query_results = dp.getDeathCauses(request.GET['Sex'], request.GET['Ethnicity'], 5)
    results_df = query_results

    # Create visualization
    fig = px.bar(results_df, # Bar chart from dataframe
            x="age_adjusted_death_rate", # X-axis
            y="leading_cause", # Y-axis
            labels=dict(age_adjusted_death_rate="Age Adjusted Death Rate per 100,000", 
            leading_cause="Top 5 Causes of Death"), # Changing label names
            color="leading_cause", # Death causes are different colors
            hover_data=["age_adjusted_death_rate"]) # hover data

    # Hide legend and allow autosize
    fig.update_traces(showlegend=False)
    fig.update_layout(autosize=True)

    # Make graph into html
    graph = fig.to_html(full_html=False)

    # Pass graph to results and render
    context = {'graph': graph}
    return render(request, 'calculator/results.html', context)



# Citywide visualization page
def visualize(request):

    # Initialize data parser model
    dp = DataParser()
    # Get citywide causes and put in dataframe
    df = dp.visualizeDeathCauses()

    # Save list of unique causes for dropdown form
    uniqueCauses = df["leading_cause"].unique() 

    # Determine y-axis range by rounding max value from dataframe and adding constant
    yAxis = df['age_adjusted_death_rate'].max()
    yAxis = round(yAxis, -1)
    yAxis = yAxis + round(yAxis * Y_AXIS_MOD, -1)

    # Create visualization
    fig = px.bar(df, # Bar chart from dataframe
            x="leading_cause", # X-axis
            y="age_adjusted_death_rate", # Y-axis
            color="race_ethnicity", # Ethnicities are different colors
            barmode='group', # Grouped bar chart
            labels=dict(age_adjusted_death_rate="Age Adjusted Death Rate per 100,000", 
            leading_cause="Cause of Death"), # Changing label names
            hover_data=["age_adjusted_death_rate", "sex", "race_ethnicity", "year"], # hover data
            facet_col="sex", # Faceted, 1 chart for each sex
            animation_frame="year", # Animate by year
            animation_group="leading_cause", # Element that animates
            range_y=[0,yAxis]) # Y-axis range

    # Set autosizing and default height
    fig.update_layout(autosize=True, height=CHART_HEIGHT)
    # Change legend title
    fig.update_layout(legend_title_text='Ethnicity')

    # Make animation bar appear lower to not conflict with labels
    fig['layout']['updatemenus'][0]['pad']=dict(r= 10, t= 150)
    fig['layout']['sliders'][0]['pad']=dict(r= 10, t= 150)

    # Update labels for male and female
    fig.for_each_annotation(lambda a: a.update(text=a.text.replace("sex=", "")))

    # Make graph into html
    graph = fig.to_html(full_html=False)

    # Pass graph and uniqueCauses to visualize and render
    context = {'graph': graph, 'uniqueCauses': uniqueCauses}
    return render(request, 'calculator/visualize.html', context)



# Comparison form page
def compareForm(request):

    # Initialize data parser model
    dp = DataParser()
    # Get citywide causes and put in dataframe
    query_results = dp.compareDeathCauses()

    # Save list of unique causes for dropdown form
    uniqueCauses = query_results["leading_cause"].unique() 

    # Pass uniqueCauses to compareForm and render
    context = {'uniqueCauses': uniqueCauses}
    return render(request, 'calculator/compareForm.html', context)



# Comparison results page
def compare(request):
    
    # Getting variables from form
    # Datapoint 1
    sex1 = request.GET['sex1']
    ethnicity1 = request.GET['ethnicity1']
    cause1 = request.GET['cause1']
    # Datapoint 2
    sex2 = request.GET['sex2']
    ethnicity2 = request.GET['ethnicity2']
    cause2 = request.GET['cause2']

    # List to show if inputted sex, ethnicity, and cause (respectively) are the same
    # 1 for same, 0 for not
    similarity = [0, 0, 0]
    similarity[0] = sex1 == sex2
    similarity[1] = ethnicity1 == ethnicity2
    similarity[2] = cause1 == cause2

    # Initialize data parser model
    dp = DataParser()
    # Get causes and put in dataframe
    df = dp.compareDeathCauses()

    # Filter data for 2 requested datapoints
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

    # Same ethnicity
    if ( similarity == [0, 1, 0] ):
        clr = "sex"
        title = "Sex"
    # Same sex, ethnicity
    if ( similarity == [1, 1, 0] ):
        clr = "leading_cause"
        title = "Cause of Death"

    # Same ethnicity, cause
    if ( similarity == [0, 1, 1] ):
        # Create visualization
        fig = px.bar(data, # Bar chart from dataframe
            x="leading_cause", # X-axis
            y="age_adjusted_death_rate", # Y-axis
            color="sex", # Sexes are different colors
            labels=dict(age_adjusted_death_rate="Age Adjusted Death Rate per 100,000", 
            leading_cause="Cause of Death"), # Changing label names
            hover_data=["age_adjusted_death_rate", "sex", "race_ethnicity", "year"], # hover data
            facet_col="sex", # Faceted, 1 chart for each sex
            animation_frame="year", # Animate by year
            animation_group="leading_cause", # Element that animates
            range_y=[0,yAxis]) # Y-axis range

        # Remove sex labels on top of each facet
        fig.for_each_annotation(lambda a: a.update(text=a.text.replace("sex=Male", "")))
        fig.for_each_annotation(lambda a: a.update(text=a.text.replace("sex=Female", "")))
        # Change legend title
        fig.update_layout(legend_title_text='Sex')

    # All other cases
    else:
        # Create visualization
        fig = px.bar(data, # Bar chart from dataframe
            x="leading_cause", # X-axis
            y="age_adjusted_death_rate", # Y-axis
            color=clr, # Set color according to variable
            labels=dict(age_adjusted_death_rate="Age Adjusted Death Rate per 100,000", 
            leading_cause="Cause of Death"), # Changing label names
            hover_data=["age_adjusted_death_rate", "sex", "race_ethnicity", "year"], # hover data
            animation_frame="year", # Animate by year
            animation_group="leading_cause", # Element that animates
            range_y=[0,yAxis]) # Y-axis range
        # Set title according to variable
        fig.update_layout(legend_title_text=title)

    # Same cause
    # Same sex, cause
    if ( (similarity == [0, 0, 1]) | (similarity == [1, 0, 1]) ):
        fig.update_layout(barmode="group")

    # Set autosizing and default height
    fig.update_layout(autosize=True, height=CHART_HEIGHT)

    # Make graph into html
    graph = fig.to_html(full_html=False)

    # Pass graph to compare and render
    context = {'graph': graph}
    return render(request, 'calculator/compare.html', context)



# City comparison page
def compareCity(request):

    # Initialize data parser model
    dp = DataParser()
    # Get data from city comparison csv
    data = dp.prepCSV()

    # Determine y-axis range by rounding  max value from dataframe and adding const
    yAxis = data['age_adjusted_death_rate'].max()
    yAxis = round(yAxis, -1)
    yAxis = yAxis + round(yAxis * Y_AXIS_MOD, -1)

    # Create visualization
    fig = px.bar(data, # Bar chart from dataframe
            x="leading_cause", # X-axis
            y="age_adjusted_death_rate", # Y-axis
            color="city", # Cities are different colors
            labels=dict(age_adjusted_death_rate="Age Adjusted Death Rate per 100,000", 
            leading_cause="Cause of Death",
            city = "City"), # Changing label names
            facet_col="sex", # Faceted, 1 chart for each sex
            animation_frame="year", # Animate by year
            animation_group="leading_cause", # Element that animates
            range_y=[0,yAxis], # Y-axis range
            barmode="group") # Grouped bar chart

    # Set autosizing and default height
    fig.update_layout(autosize=True, height=CHART_HEIGHT)

    # Make animation bar appear lower to not conflict with labels
    fig['layout']['updatemenus'][0]['pad']=dict(r= 10, t= 150)
    fig['layout']['sliders'][0]['pad']=dict(r= 10, t= 150)

    # Update labels for male and female
    fig.for_each_annotation(lambda a: a.update(text=a.text.replace("sex=", "")))
    fig.for_each_annotation(lambda a: a.update(text=a.text.replace("oslo", "Oslo")))

    # Make graph into html
    graph = fig.to_html(full_html=False)

    # Pass graph to compareCity and render
    context = {'graph': graph}
    return render(request, 'calculator/compareCity.html', context)



# Site bibliography
def bib(request):
    return render(request, 'calculator/bib.html')