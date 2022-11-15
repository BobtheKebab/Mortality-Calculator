from django.test import TestCase
from calculator.models import DataParser
from sodapy import Socrata
import pandas as pd


data_url = 'data.cityofnewyork.us'  # The Host Name for the API endpointy)
data_set = 'jb7j-dtam'  # The data set at the API endpoint
app_token = 'GI8oZAztXFWG3uda2SXGB1jGn'  # The app token created in the prior steps

class GetResultTestCase(TestCase):
    def setUp(self):
        self.client = Socrata(data_url, app_token)

    def testInvalidInput(self):
        sex = "Female"
        ethnicity = "White"
        limit = 5
        payload_noSex = "year = '2019' AND sex = '" + "" + "' AND race_ethnicity = '" + ethnicity + "'"
        payload_noEthnicity = "year = '2019' AND sex = '" + sex + "' AND race_ethnicity = '" + "" + "'"
        cols = "leading_cause, deaths, age_adjusted_death_rate"

        results_noSex = self.client.get(data_set, limit=limit, where=payload_noSex, select=cols)
        results_noEthnicity = self.client.get(data_set, limit=limit, where=payload_noEthnicity, select=cols)
        results_noLimit = self.client.get(data_set, limit=None, where=payload_noEthnicity, select=cols)

        results_df_noSex = pd.DataFrame.from_records(results_noSex)
        results_df_noEthnicity = pd.DataFrame.from_records(results_noEthnicity)
        results_df_noLimit = pd.DataFrame.from_records(results_noLimit)

        #This will test when we have only 1 input which is sex
        self.assertEqual(DataParser.cleanDataFrame(results_df_noSex).empty, True)
        #This will test when we have only 1 input which is ethnicity
        self.assertEqual(DataParser.cleanDataFrame(results_df_noEthnicity).empty, True)
        #This will test when we have only 1 input which is limit
        self.assertEqual(DataParser.cleanDataFrame(results_df_noLimit).empty, True)



    def testValidInput(self):
        sex = "Male"
        ethnicity = "Non-Hispanic White"
        limit = 5
        payload = "year = '2019' AND sex = '" + sex + "' AND race_ethnicity = '" + ethnicity + "'"
        cols = "leading_cause, deaths, age_adjusted_death_rate"

        results = self.client.get(data_set, limit=limit, where=payload, select=cols)

        results_df = pd.DataFrame.from_records(results)

        result = DataParser.cleanDataFrame(results_df)
        #This should return a non empty result
        #check that the limit is equal to the parameter
        self.assertEqual(result.empty, False)
        self.assertEqual(len(result), 5)

    

    def testVisualizeDeathCauses(self):
        result = DataParser.visualizeDeathCauses(self)
        #This should return a non empty result
        self.assertEqual(result.empty, False)
        #check that the limit is equal to 20
        self.assertEqual(len(result),20)



    def testCleanDataFrame(self):

        # Check parenthases removal
        dataTest = {'sex': ['A()', 'B()', 'C()']}
        dfTest = pd.DataFrame(dataTest, columns=['sex'])

        data = {'sex': ['A', 'B', 'C']}
        df = pd.DataFrame(data, columns=['sex'])

        dfTest = DataParser.cleanDataFrame(dfTest)
        df = DataParser.cleanDataFrame(df)

        self.assertEqual(df.equals(dfTest), True)

        # Check truncation
        dataTest = {'sex': ['A_______________________________________+++++', 'B', 'C']}
        dfTest = pd.DataFrame(dataTest, columns=['sex'])

        data = {'sex': ['A_______________________________________...', 'B', 'C']}
        df = pd.DataFrame(data, columns=['sex'])

        dfTest = DataParser.cleanDataFrame(dfTest)
        df = DataParser.cleanDataFrame(df)

        self.assertEqual(df.equals(dfTest), True)