from django.test import TestCase 
from calculator.models import DataParser
import pandas as pd

class GetResultTestCase(TestCase):
    def test_getResult(self):
        sex = "Female"
        ethnicity = "White"
        limit = 5
        #This will test when we have only 1 input which is sex
        self.assertEqual(DataParser.getDeathCauses(sex, None, limit), None)
        #This will test when we have only 1 input which is ethnicity
        self.assertEqual(DataParser.getDeathCauses(None, ethnicity, limit), None)
        #This will test when we have only 1 input which is limit
        self.assertEqual(DataParser.getDeathCauses(sex, ethnicity, None), None)
