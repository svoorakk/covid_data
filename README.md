# covid_data
Code to download ECDC &amp; John Hopkins Univ. COVID Data and save to csv files.

- Run `data_download_ecdc.py` to get ECDC data.

- Run `data_download_jh.py` to get John Hopkins University data. JH data is in separate data files for each day. The code executes a loop to get data for all days and saves data for all days into one csv file. If a csv file with same name already exists, it is read to find the last update and does a incremental update.
