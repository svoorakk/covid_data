"""
Module to fetch daily COVID data from ECDC website and save as local csv
"""
import os
import pandas as pd

ECDC_CSV_URL = 'https://opendata.ecdc.europa.eu/covid19/casedistribution/csv'

ecdc_path = 'ecdc_data.csv'

os.environ['HTTP_PROXY'] = '' # Set the proxy if required
os.environ['HTTPS_PROXY'] = '' # Set the proxy if required

ecdc_data = pd.read_csv(ECDC_CSV_URL)
ecdc_data.to_csv(ecdc_path)
