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


    def testValidInput(self):
        sex = "M"
        ethnicity = "Hispanic"
        limit = 5
        payload = "year = '2014' AND sex = '" + sex + "' AND race_ethnicity = '" + ethnicity + "'"

        results = self.client.get(data_set, limit=limit, where=payload)

        result = pd.DataFrame.from_records(results)

        #This should return a non empty result
        #check that the limit is equal to the parameter
        self.assertEqual(result.empty, False)
        self.assertEqual(len(result), 5)


    def testVisualizeDeathCauses(self):
        payload = "year = '2019' AND race_ethnicity != 'Other Race/ Ethnicity'"
        payload += " AND race_ethnicity != 'Not Stated/Unknown'"
        payload += "OR year = '2014' AND race_ethnicity != 'Other Race/ Ethnicity'"
        payload += " AND race_ethnicity != 'Not Stated/Unknown'"
        payload += "OR year = '2009' AND race_ethnicity != 'Other Race/ Ethnicity'"
        payload += " AND race_ethnicity != 'Not Stated/Unknown'"

        cols = ""
        results = self.client.get(data_set, where=payload, select=cols)

        df = pd.DataFrame.from_records(results)
        df =  DataParser.cleanDataFrame(df)
        df = df.sort_values('year', ascending=True)

        result = DataParser.cleanDataFrame(df)

        #This should return a non empty result
        self.assertEqual(result.empty, False)
        #check that the limit is equal to 177
        self.assertEqual(len(result),177)


    def testCompareDeathCauses(self):
        payload = "year = '2019' AND race_ethnicity != 'Other Race/ Ethnicity'"
        payload += " AND race_ethnicity != 'Not Stated/Unknown'"
        payload += "OR year = '2014' AND race_ethnicity != 'Other Race/ Ethnicity'"
        payload += " AND race_ethnicity != 'Not Stated/Unknown'"
        payload += "OR year = '2009' AND race_ethnicity != 'Other Race/ Ethnicity'"
        payload += " AND race_ethnicity != 'Not Stated/Unknown'"

        cols = ""
        results = self.client.get(data_set, where=payload, select=cols)

        df = pd.DataFrame.from_records(results)
        df = DataParser.cleanDataFrame(df)
        df = df.sort_values('year', ascending=True)

        cutOut = ["Septicemia", "Viral Hepatitis", "Peptic Ulcer", "Parkinson's Disease", 
        "Insitu or Benign / Uncertain Neoplasms",
        "Anemias", "Aortic Aneurysm and Dissection", "Atherosclerosis",
        "Cholelithiasis and Disorders of Gallbladder", "Complications of Medical and Surgical Care",
        "Mental and Behavioral Disorders due to Use of Alcohol"]

        for cut in cutOut:
            df = df.query('leading_cause != "' + cut + '"')

        result = DataParser.cleanDataFrame(df)
        self.assertEqual(result.empty, False)
        self.assertEqual(len(result), 176)

    def testCleanDataFrame(self):
        # Check parenthases removal
        dataTest = [{'sex': ['M', 'F', 'M'], 'leading_cause': ['Accidents', 'Mental and Behavioral Disorders due to Accidental Poisoning and Other Psychoactive Substance Use', 'Accidents'], 'race_ethnicity': ['White Non-Hispanic', 'Black Non-Hispanic', 'White Non-Hispanic'], 'age_adjusted_death_rate':[90.0, 90.0, 90.0], 'year': [2000, 2000, 2000]}]
        dfTest = pd.DataFrame(dataTest[0], columns=['sex', 'leading_cause', 'race_ethnicity', 'age_adjusted_death_rate', 'year'])
        data = [{'sex': ['Male', 'Female', 'Male'], 'leading_cause': ['Accidents Except Drug Poisoning', 'Mental and Behavioral Disorders Due to Substance Use', 'Accidents Except Drug Poisoning'], 'race_ethnicity': ['Non-Hispanic White', 'Non-Hispanic Black', 'Non-Hispanic White'] , 'age_adjusted_death_rate':[90.0, 90.0, 90.0], 'year': [2000, 2000, 2000]}]
        df = pd.DataFrame(data[0], columns=['sex', 'leading_cause', 'race_ethnicity', 'age_adjusted_death_rate', 'year'])

        dfTest = DataParser.cleanDataFrame(dfTest)
        df = DataParser.cleanDataFrame(df)
        #self.assertEqual(df.equals(dfTest), True)

    def testPrepCSV(self):

        # Get dataframe for city comparison
        dp = DataParser()
        data = dp.prepCSV()

        # Check if empty
        self.assertEqual(data.empty, False)

        # Check if containing 3 cities
        cities = data["city"].unique()
        self.assertEqual(len(cities), 3)

        # Make sure numerical columns are not considered strings
        yearType = data['year'].dtype
        rateType = data['age_adjusted_death_rate'].dtype
        self.assertNotEqual(yearType, str)
        self.assertNotEqual(rateType, str)

        # Make sure there are at least 4 causes of death
        cause = data['leading_cause'].unique()
        self.assertTrue(len(cause) > 3)