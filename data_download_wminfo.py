"""
This script scrapes worldmeters.info covid page and saves country wise stats
to a csv file
"""
from bs4 import BeautifulSoup
import pickle
import requests
import datetime
from csv import writer

LOCAL_DT_TM_FMT = '%d/%m/%Y %H:%M:%S'
OUT_FILE_PATH = 'wminfo.csv'

# Get html content
url = 'https://www.worldometers.info/coronavirus/'
# to mock a browser
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
response = requests.get(url, headers=headers)
html = response.content

# Parse html to extract country wise data
data = []
soup = BeautifulSoup(html, 'html.parser')
ctry_tabl = soup.find(id='main_table_countries_today')
col_names = ['UpdateTime', 'Country_Other', 'TotalCases', 'NewCases', 'TotalDeaths', 'NewDeaths', 'TotalRecovered',
             'ActiveCases', 'Serious,Critical', 'Tot Cases per 1M pop', 'Deaths per 1M pop', 'TotalTests',
             'Tests per 1M pop']
# to derive col names from data uncomment below 2 lines
# vcol_names = ['DateTime']+ \
#            [cell.text.strip().replace('\n','') for cell in ctry_tabl.find('thead').find('tr').find_all('th')]
data.append(col_names)

# for populating values in UpdateTime column.
time = datetime.datetime.now().strftime(LOCAL_DT_TM_FMT)

tbody_rows = ctry_tabl.find('tbody').find_all('tr')
for row in tbody_rows:
    cells = row.find_all('td')
    row_data = [time]
    for i, cell in enumerate(cells):
        txt = cell.text.strip().replace(',','')
        if i in [1,2,3,4,5,6,7,10]:
            val = int(txt) if len(txt) > 0 else ''
        elif i in [8,9,11]:
            val = float(txt) if len(txt) > 0 else ''
        else:
            val = txt
        row_data.append(val)
    data.append(row_data)

with open(OUT_FILE_PATH, 'w', newline='') as f:
    csv_writer = writer(f, delimiter=',')
    csv_writer.writerows(data)
