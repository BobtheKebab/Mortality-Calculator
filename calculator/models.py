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
        #payload += " OR year = '2009' AND race_ethnicity != 'Other Race/ Ethnicity' AND race_ethnicity != 'Not Stated/Unknown'"
        results = self.client.get(data_set, where=payload)

        results_df = pd.DataFrame.from_records(results)
        return self.cleanDataFrame(results_df)



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

            df['leading_cause'][i] = cause
            
            # Standardize sex column
            sex = df['sex'][i]
            if (sex == 'M'):
                sex = "Male"
            elif (sex == 'F'):
                sex = "Female"
            df['sex'][i] = sex

            ethnicity = df['race_ethnicity'][i]
            if (ethnicity == 'White Non-Hispanic'):
                ethnicity = 'Non-Hispanic White'
            elif (ethnicity == 'Black Non-Hispanic'):
                ethnicity = 'Non-Hispanic Black'
            df['race_ethnicity'][i] = ethnicity

        # Make aa death rate a float and sort descending
        df = df.astype({"age_adjusted_death_rate": float})
        df = df.sort_values(by=['age_adjusted_death_rate'], ascending=False)

        return df