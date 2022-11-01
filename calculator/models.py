from django.db import models #noqa
import pandas as pd
from sodapy import Socrata

data_url = 'data.cityofnewyork.us'  # The Host Name for the API endpointy)
data_set = 'jb7j-dtam'  # The data set at the API endpoint
app_token = 'GI8oZAztXFWG3uda2SXGB1jGn'  # The app token created in the prior steps

class DataParser:

    def __init__(self):
        self.client = Socrata(data_url, app_token)



    def getDeathCauses(self, pSex, pEthnicity, pLimit):

        if (pEthnicity is None):
            return None
        if (pSex is None):
            return None
        if (pLimit is None):
            return None

        payload = "year = '2019' AND sex = '" + pSex + "' AND race_ethnicity = '" + pEthnicity + "'"
        cols = "leading_cause, deaths, age_adjusted_death_rate"
        results = self.client.get(data_set, limit=pLimit, where=payload, select=cols)
        #, order="age_adjusted_death_rate DESC")

        results_df = pd.DataFrame.from_records(results)
        return results_df



    def visualizeDeathCauses(self):
        
        payload = ""
        #cols = "year, leading_cause, deaths, age_adjusted_death_rate"
        cols = ""
        results = self.client.get(data_set, limit=20, where=payload, select=cols)
        #, order="age_adjusted_death_rate DESC")

        results_df = pd.DataFrame.from_records(results)

        return results_df