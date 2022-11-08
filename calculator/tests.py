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
        #This will test when we have only 1 input which is sex
        self.assertEqual(DataParser.getDeathCauses(self, sex,None, limit), None)
        #This will test when we have only 1 input which is ethnicity
        self.assertEqual(DataParser.getDeathCauses(self, None, ethnicity, limit), None)
        #This will test when we have only 1 input which is limit
        self.assertEqual(DataParser.getDeathCauses(self, sex, ethnicity, None), None)



    def testValidInput(self):
        sex = "Male"
        ethnicity = "Non-Hispanic White"
        limit = 5
        result = DataParser.getDeathCauses(self, sex, ethnicity, limit)
        #This should return a non empty result
        self.assertEqual(result.empty, False)
        #check that the limit is equal to the parameter
        self.assertEqual(len(result),5)

    

    def testVisualizeDeathCauses(self):
        result = DataParser.visualizeDeathCauses(self)
        #This should return a non empty result
        self.assertEqual(result.empty, False)
        #check that the limit is equal to 20
        self.assertEqual(len(result),20)



    def testCleanDataFrame(self):
        dataTest = {'leading_cause': ['A()', 'B()', 'C()']}
        dfTest = pd.DataFrame(dataTest, columns=['leading_cause'])

        data = {'leading_cause': ['A', 'B', 'C']}
        df = pd.DataFrame(data, columns=['leading_cause'])

        self.assertEqual(dfTest, df)