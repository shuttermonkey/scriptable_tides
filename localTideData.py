#!/usr/bin/python3

# script pulls and consolidates relevant data columns from NOAA tide files
# .txt filesdownloaded from
# https://tidesandcurrents.noaa.gov/noaatideannual.html?id=8468448
# each file is different year, MLLW Datum, 12H clock, GMT timezone, format TXT 

import pandas as pd
import datetime

import os
from dotenv import load_dotenv
load_dotenv()

def main():
    #variables run this to aggregate three years of tide data...
    fileNames = ["8468448_annual-5.txt", "8468448_annual-6.txt", "8468448_annual-7.txt"]
    sourceDir = os.getenv('SOURCE_DIR')
    exportName = sourceDir + 'tides_2021-2023.csv'

    #import files, create dataframe and make timezone aware
    df = pd.DataFrame() 

    for i in fileNames:
        filename = sourceDir + i
        df = df.append(pd.read_csv(filename, skiprows=13, sep='\t+', header=0, engine='python'))

    #remove white space from column headings
    df.columns = df.columns.str.strip()

    # convert Date Day Time to timestamp with UTC timezone
    df['Timestamp'] = pd.to_datetime(df['Date'] + ' ' + df['Time'],utc=True)

    #save consolidated file  
    export_file = df[['Timestamp','High/Low','Pred(Ft)','Pred(cm)']]
    export_file = export_file.to_csv(exportName, index=False)

if __name__ == "__main__":
    main()