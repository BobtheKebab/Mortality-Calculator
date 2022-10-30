from django.test import TestCase 
from calculator.models import DataParser
import pandas as pd

class GetResultTestCase(TestCase):
    def testInvalidInput(self):
        sex = "Female"
        ethnicity = "White"
        limit = 5
        #This will test when we have only 1 input which is sex
        self.assertEqual(DataParser.getDeathCauses(sex,None, limit), None)
        #This will test when we have only 1 input which is ethnicity
        self.assertEqual(DataParser.getDeathCauses(None, ethnicity, limit), None)
        #This will test when we have only 1 input which is limit
        self.assertEqual(DataParser.getDeathCauses(sex, ethnicity, None), None)

    def testValidInput(self):
        sex = "Male"
        ethnicity = "Non-Hispanic White"
        limit = 5
        result = DataParser.getDeathCauses(sex,ethnicity,limit)
        #This should return a non empty result
        self.assertEqual(result.empty, False)
        #check that the limit is equal to the parameter
        self.assertEqual(len(result),5)



