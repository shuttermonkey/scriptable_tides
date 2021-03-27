#!/usr/bin/python3

import pandas as pd
import paramiko
import json

from datetime import date, datetime, timedelta, time, timezone
import pytz
local_timezone = pytz.timezone("US/Eastern")

import os
from dotenv import load_dotenv
load_dotenv()

def main():
    sourceDir = os.getenv('SOURCE_DIR')
    importFile = sourceDir + 'tides_2021-2023.csv'

    df = pd.read_csv(importFile)

    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    df['LocalTimestamp'] = df['Timestamp'].apply(lambda x:x.tz_convert('US/Eastern'))

    myJson = {}
    myJson['tideLevel'] = tidePercent(df=df)
    myJson['nextTide'] = nextTide(df=df)['tide'].replace('H','High').replace('L','Low')
    myJson['nextTideTime'] = nextTide(df=df)['time'].strftime('%I:%M %p')
    myJson['updated'] = datetime.now().astimezone(local_timezone).strftime('%m-%d-%Y %I:%M %p')
    myJson['todaysTides'] = todaysTides(df=df)
    #print(myJson)
    ftp_file(json.dumps(myJson))
    print(json.dumps(myJson))


def nextTide(df, dateTime = datetime.now(timezone.utc)):
    # returns a dict of localtime, tide, height
    df_row = df[(df['Timestamp'] > dateTime)].head(1).to_numpy() #select df row and convert to array
    return ({'time': df_row[0][4], 'tide': df_row[0][1], 'height': df_row[0][2]})
    

def prevTide(df, dateTime = datetime.now(timezone.utc)):
    # add in return types so we can return height, tide type etc if wanted
    df = df.sort_values(['Timestamp'], ascending=[False])
    df_row = df[(df['Timestamp'] <= dateTime)].head(1).to_numpy() #select df row and convert to array
    return ({'time': df_row[0][4], 'tide': df_row[0][1], 'height': df_row[0][2]})

def nextHiTide(df, dateTime = datetime.now(timezone.utc)):
    # returns a dict of localtime, tide, height
    df_row = df[(df['Timestamp'] > dateTime) & (df['High/Low'] == "H")].head(1).to_numpy() #select df row and convert to array
    return ({'time': df_row[0][4], 'tide': df_row[0][1], 'height': df_row[0][2]})

def todaysTides(df, dateTime = datetime.now().astimezone(local_timezone)):
    t_start = dateTime.replace(hour=0,minute=0, second=0)
    t_end = dateTime.replace(hour=23,minute=59, second=0)
    df['Tides'] = df['High/Low'].replace({'H':'High', 'L':'Low'})
    df['time'] = df['LocalTimestamp'].apply(lambda x: x.strftime('%I:%M %p'))
    df = df[['LocalTimestamp', 'Tides', 'Pred(Ft)','time']]
    df.columns = ['LocalTimestamp','tide','height','time']
    df = (df[(df['LocalTimestamp'] >= t_start) & (df['LocalTimestamp'] <= t_end)])
    df = df.drop(columns=['LocalTimestamp'])
    return df.to_dict('records')


def tidePercent (df, dateTime = datetime.now().astimezone(local_timezone)):
    #returns tide percentage between -100 (low) and +100 (high)
    t_now = datetime.now(timezone.utc)
    t_last = prevTide(df, dateTime)['time']
    t_next = nextTide(df, dateTime)['time']
    t_total = t_next-t_last
    t_pct = (dateTime - t_last) / t_total
    if prevTide(df, t_now)['tide'] == "H":
        t_pct = 1-t_pct    
    return(round(2*((t_pct*100)-50))) #should be -100 to +100

def ftp_file(json):
    user = os.getenv('FTP_USER')
    pw = os.getenv('FTP_PW')
    host = os.getenv('FTP_URL')
    port = 22
    transport = paramiko.Transport((host, port))
    transport.connect(username = user, password = pw)
    sftp = paramiko.SFTPClient.from_transport(transport)
    with sftp.open('todays_tides.json', "w") as f:
        f.write(json)
    sftp.close()
    transport.close()
    print ('done.')

if __name__ == "__main__":
    main()

