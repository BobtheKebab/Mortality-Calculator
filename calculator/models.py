from django.db import models #noqa
import pandas as pd
from sodapy import Socrata
import re

data_url = 'data.cityofnewyork.us'  # The Host Name for the API endpointy)
data_set = 'jb7j-dtam'  # The data set at the API endpoint
app_token = 'GI8oZAztXFWG3uda2SXGB1jGn'  # The app token created in the prior steps

class DataParser:

    def __init__(self):
        self.client = Socrata(data_url, app_token)



    # Get death data for specific ethnicity and sex (results page)
    def getDeathCauses(self, pSex, pEthnicity, pLimit):

        if (pEthnicity is None):
            return None
        if (pSex is None):
            return None
        if (pLimit is None):
            return None
        
        payload = "year = '2019' AND sex = '" + pSex + "' AND race_ethnicity = '" + pEthnicity + "'"
        results = self.client.get(data_set, limit=pLimit, where=payload)
        
        results_df = pd.DataFrame.from_records(results)
        return self.cleanDataFrame(results_df)


    
    # Get death data for all categories (visualize page)
    def visualizeDeathCauses(self):

        payload = "year = '2019' AND race_ethnicity != 'Other Race/ Ethnicity' AND race_ethnicity != 'Not Stated/Unknown'"
        payload += "OR year = '2014' AND race_ethnicity != 'Other Race/ Ethnicity' AND race_ethnicity != 'Not Stated/Unknown'"
        payload += "OR year = '2009' AND race_ethnicity != 'Other Race/ Ethnicity' AND race_ethnicity != 'Not Stated/Unknown'"

        cols = ""
        results = self.client.get(data_set, where=payload, select=cols)

        df = pd.DataFrame.from_records(results)
        df = self.cleanDataFrame(df)
        df = df.sort_values('year', ascending=True)

        cutOut = ["Septicemia ", "Viral Hepatitis ", "Peptic Ulcer ", "Parkinson's Disease ", "Insitu or Benign / Uncertain Neoplasms ",
        "Anemias ", "Aortic Aneurysm and Dissection ", "Atherosclerosis ",
        "Cholelithiasis and Disorders of Gallbladder ", "Complications of Medical and Surgical Care ",
        "Mental and Behavioral Disorders due to Use of Alcohol "]

        for cut in cutOut:
            df = df.query('leading_cause != "' + cut + '"')

        return self.cleanDataFrame(df)



    # Clean data before it gets displayed
    @staticmethod
    def cleanDataFrame(df):

        exp = "\(.*?\)" # Remove everything between parentheses
        maxLength = 40; # Max length of label on graph

        for i in df.index:
            cause = df['leading_cause'][i]

            # Apply regex
            cause = re.sub(exp, "", cause)
            # Changing especially long label
            if "Mental" in cause:
                cause = "Mental and Behavioral Disorders Due to Substance Use"
                
            if "Accidents" in cause:
                cause = "Accidents Except Drug Poisoning"

            df['leading_cause'][i] = cause
            
            # Standardize sex column
            sex = df['sex'][i]
            if (sex == 'M'):
                sex = "Male"
            elif (sex == 'F'):
                sex = "Female"
            df['sex'][i] = sex
            
            # Standardize ethnicity column
            sex = df['race_ethnicity'][i]
            if (sex == 'White Non-Hispanic'):
                sex = "Non-Hispanic White"
            elif (sex == 'Black Non-Hispanic'):
                sex = "Non-Hispanic Black"
            df['race_ethnicity'][i] = sex

        df = df.astype({"age_adjusted_death_rate": float})
        df = df.astype({"year": int})

        return df