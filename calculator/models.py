from django.db import models #noqa
import pandas as pd
from sodapy import Socrata

class DataParser:

    @staticmethod
    def getDeathCauses(pSex, pEthnicity, pLimit):
        if (pEthnicity == None or pSex == None or pLimit == None):
            return None
            
        data_url = 'data.cityofnewyork.us'  # The Host Name for the API endpointy)
        data_set = 'jb7j-dtam'  # The data set at the API endpoint
        app_token = 'GI8oZAztXFWG3uda2SXGB1jGn'  # The app token created in the prior steps
        client = Socrata(data_url, app_token)

        payload = "year = '2019' AND sex = '" + pSex + "' AND race_ethnicity = '" + pEthnicity + "'"
        cols = "leading_cause, deaths, age_adjusted_death_rate"
        results = client.get(data_set, limit=pLimit, where=payload, select=cols)
        #, order="age_adjusted_death_rate DESC")

        results_df = pd.DataFrame.from_records(results)

        return results_df