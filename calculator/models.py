from django.db import models #noqa
import pandas as pd
from sodapy import Socrata

class DataParser:

    @staticmethod
    def getDeathCauses(pSex, pEthnicity, pLimit):
        data_url = 'data.cityofnewyork.us'  # The Host Name for the API endpointy)
        data_set = 'jb7j-dtam'  # The data set at the API endpoint
        app_token = 'GI8oZAztXFWG3uda2SXGB1jGn'  # The app token created in the prior steps
        client = Socrata(data_url, app_token)

        payload = "year = '2019' AND sex = '" + pSex + "' AND race_ethnicity = '" + pEthnicity + "'"
        results = client.get(data_set, limit=pLimit, where=payload, order="age_adjusted_death_rate DESC")

        results_df = pd.DataFrame.from_records(results)

        return results_df