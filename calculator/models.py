from django.db import models #noqa
import pandas as pd
from sodapy import Socrata
import re

data_url = 'data.cityofnewyork.us'  # The Host Name for the API endpoint
data_set = 'jb7j-dtam'  # The data set at the API endpoint
app_token = 'GI8oZAztXFWG3uda2SXGB1jGn'  # The app token created in the prior steps

class DataParser:



    # Initialize a connection to API client
    def __init__(self):
        self.client = Socrata(data_url, app_token)



    # Get death data for specific ethnicity and sex (results page)
    def getDeathCauses(self, pSex, pEthnicity, pLimit):

        # Do not query for data if parameters are missing
        if (pEthnicity is None):
            return None
        if (pSex is None):
            return None
        if (pLimit is None):
            return None
        
        # Get data where year is 2014, pSex, pEthnicity
        payload = "year = '2014' AND sex = '" + pSex + "' AND race_ethnicity = '" + pEthnicity+"'"
        payload += " AND leading_cause != 'All Other Causes'"
        results = self.client.get(data_set, limit=pLimit, where=payload)
        
        # Create a dataframe from queried data and return it
        results_df = pd.DataFrame.from_records(results)
        return self.cleanDataFrame(results_df)


    
    # Get death data for all categories (visualize page)
    def visualizeDeathCauses(self):

        # Getting data for 2014 and 2009, excluding unknown and other ethnicities
        payload = "year = '2014' AND race_ethnicity != 'Other Race/ Ethnicity'"
        payload += " AND race_ethnicity != 'Not Stated/Unknown'"
        payload += "OR year = '2009' AND race_ethnicity != 'Other Race/ Ethnicity'"
        payload += " AND race_ethnicity != 'Not Stated/Unknown'"

        # Results of API call
        results = self.client.get(data_set, where=payload)

        # Create dataframe from results, clean it, and sort it by year
        df = pd.DataFrame.from_records(results)
        df = self.cleanDataFrame(df)
        df = df.sort_values('year', ascending=True)
        
        # Filter dataframe for causes we choose (top 5 excluding other)
        df = df[ (df.leading_cause == "Diseases of Heart")
        | (df.leading_cause == "Malignant Neoplasms")
        | (df.leading_cause == "Diabetes Mellitus")
        | (df.leading_cause == "Influenza and Pneumonia")
        | (df.leading_cause == "Cerebrovascular Disease")]

        # Clean dataframe and return it
        return self.cleanDataFrame(df)

    # Get data for comparison page
    def compareDeathCauses(self):

        # Getting data for 2014 and 2009, excluding unknown and other ethnicities
        payload = "year = '2014' AND race_ethnicity != 'Other Race/ Ethnicity'"
        payload += " AND race_ethnicity != 'Not Stated/Unknown'"
        payload += "OR year = '2009' AND race_ethnicity != 'Other Race/ Ethnicity'"
        payload += " AND race_ethnicity != 'Not Stated/Unknown'"

        # Results of API call
        results = self.client.get(data_set, where=payload)

        # Create dataframe from results, clean it, and sort it by year
        df = pd.DataFrame.from_records(results)
        df = self.cleanDataFrame(df)
        df = df.sort_values('year', ascending=True)

        # List of causes we want to remove from data
        cutOut = ["Septicemia", "Viral Hepatitis", "Peptic Ulcer", "Parkinson's Disease", 
        "Insitu or Benign / Uncertain Neoplasms",
        "Anemias", "Aortic Aneurysm and Dissection", "Atherosclerosis",
        "Cholelithiasis and Disorders of Gallbladder","Complications of Medical and Surgical Care",
        "Mental and Behavioral Disorders due to Use of Alcohol"]

        # Remove specified causes from dataframe
        for cut in cutOut:
            df = df.query('leading_cause != "' + cut + '"')

        # Clean dataframe and return it
        return self.cleanDataFrame(df)



    # Clean data before it gets displayed
    @staticmethod
    def cleanDataFrame(df):

        # Remove everything between parentheses and preceding whitespace
        exp = r"\s+\(.*?\)" 

        # Go through every member of dataframe
        for i in df.index:

            # Get death cause for data member
            cause = df['leading_cause'][i]

            # Apply regex
            cause = re.sub(exp, "", cause)

            # Changing especially long label
            if '''Mental and Behavioral Disorders due to Accidental
                Poisoning and Other Psychoactive Substance Use''' in cause:
                cause = "Mental and Behavioral Disorders Due to Substance Use"
                
            # Changing accidents label
            if "Accidents" in cause:
                cause = "Accidents Except Drug Poisoning"

            # Assign changed death cause
            df['leading_cause'][i] = cause

        # Make death rate column float and year column int
        df = df.astype({"age_adjusted_death_rate": float})
        df = df.astype({"year": int})

        # Return cleaned data
        return df



    # Get data for city compare page
    def prepCSV(self):

        # Read from city comparison csv
        data = pd.read_csv('staticfiles/calculator/cities.csv')
        # Exclude 2009 data
        data = data[ (data.year != 2009)]
        # Sort data by year
        data = data.sort_values('year', ascending=True)

        return data