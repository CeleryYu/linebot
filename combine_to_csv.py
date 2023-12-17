# -*- coding: utf-8 -*-
"""
Created on Sun Dec 17 17:34:22 2023

@author: N3D
"""

import pandas as pd
import datetime
import schedule
import time
from IPython import get_ipython
import pygsheets

gc = pygsheets.authorize(service_file='C:/Users/N3D/Downloads/linebot-408306-c24b0b63b2cf.json')
sht = gc.open_by_url('https://docs.google.com/spreadsheets/d/1TLRVLW0s9wKxAnvw8yQjBM3r19hWrtVjsPOMeOW73Ts/')

def process_google_sheets_data():
    # Step 1: Identify all sheets in the Google Sheets
    sheets = sht.worksheets()

    # Step 2: Read each sheet and extract the last row
    last_rows = []
    for sheet in sheets:
        df = sheet.get_as_df(start='B1', empty_value='', include_tailing_empty=False)
        Name = sheet.title
        last_row = df.iloc[-1].copy()  # Extract the last row
        if datetime.datetime.strptime(last_row['date'], '%Y-%m-%d').date() != datetime.datetime.today().date():
            last_row[:] = 'NA'
        last_row['姓名'] = Name
        last_rows.append(last_row)

    # Step 3: Combine the last rows into a single DataFrame
    result_df = pd.concat(last_rows, axis=1).T

    # Reset index to create a new set of continuous integers
    result_df.reset_index(drop=True, inplace=True)
    result_df = result_df.drop(columns=['date'])

    # Save the result as a new CSV file without the original headers
    current_date = datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=8))).date()
    formatted_today = current_date.strftime('%Y-%m-%d')
    file_name = f"{formatted_today}.csv"
    result_df.to_csv(file_name, index=True)

try:
    # Clear the preceding schedules
    schedule.clear()
    #schedule.every(15).seconds.do(process_google_sheets_data)
    schedule.every().day.at('6:30').do(process_google_sheets_data)

    # Run the scheduler
    while True:
        schedule.run_pending()
        time.sleep(1)
        
except Exception as e:
    print(f"Error occurred: {e}")
    # Clear Spyder console
    get_ipython().magic('clear')
