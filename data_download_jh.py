"""
Module to fetch daily COVID data from John Hopkins University
github repo https://github.com/CSSEGISandData/COVID-19
"""

import pandas as pd
import os
import time
from datetime import date, timedelta

LOCAL_DT_FMT = '%d/%m/%Y'
LOCAL_DT_TM_FMT = '%d/%m/%Y %H:%M:%S'
JH_DATA_DT_FMT = "%m-%d-%Y"

os.environ['HTTP_PROXY'] = '' # Set the proxy if required
os.environ['HTTPS_PROXY'] = '' # Set the proxy if required

jh_data_base_url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/" \
                   "csse_covid_19_data/csse_covid_19_daily_reports/%s.csv"


jh_path = 'jh_data.csv'
jh_data = pd.DataFrame()

start_date = date(2020, 1, 22)
if os.path.exists(jh_path):  # If the data file exists, set the start date for incremental update
    jh_data = pd.read_csv(jh_path, index_col=0)
    jh_data.reset_index()
    ser = jh_data['data_date']
    ser = pd.to_datetime(ser, infer_datetime_format=True)
    start_date = max(ser) + timedelta(days=1) # Get the max date and add 1 day to set start date

data_date = start_date
data_arr = [jh_data]
# get data for all the days
while data_date < date.today():
    url = jh_data_base_url % data_date.strftime(JH_DATA_DT_FMT)
    print(url)
    time.sleep(1)
    data = pd.read_csv(url)
    cols = data.columns
    # Column names change as days progress. Renaming columns so that data frames can be concatenated properly
    if len(cols)  == 6:
        cols = ['Province_State', 'Country_Region', 'Last_Update', 'Confirmed', 'Deaths', 'Recovered']
    if 'Latitude' in cols:
        cols = ['Province_State', 'Country_Region', 'Last_Update', 'Confirmed', 'Deaths', 'Recovered', 'Lat', 'Long_']
    data.columns = cols
    ser = pd.to_datetime(data['Last_Update'], infer_datetime_format=True)
    ser = ser.apply(lambda x: x.strftime(LOCAL_DT_TM_FMT))
    data['Last_Update'] = ser
    data['data_date'] = data_date.strftime(LOCAL_DT_FMT)
    data_arr.append(data)
    data_date = data_date + timedelta(days=1)

jh_data = pd.concat(data_arr)
jh_data.to_csv(os.path.join('..', '..', 'downloads', 'jh_data.csv'))

