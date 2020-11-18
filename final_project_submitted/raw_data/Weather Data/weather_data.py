#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 22 16:32:07 2020

@author: saraborchers
"""
import pandas as pd
from datetime import datetime, timedelta


def isnumber(x):
    try:
        float(x)
        return True
    except:
        return False
    
df = pd.read_csv('2354137.csv',low_memory=False)
df = df[['STATION','DATE','HourlyDryBulbTemperature','HourlyRelativeHumidity','HourlyWetBulbTemperature']]
df['DateTime']=pd.to_datetime(df['DATE']).dt.round('H')
df = df.drop(['DATE'],axis=1)
df = df[['STATION','DateTime','HourlyDryBulbTemperature','HourlyRelativeHumidity','HourlyWetBulbTemperature']]


stations = df.STATION.unique()
df_dict = {elem : pd.DataFrame for elem in stations}
for key in df_dict.keys():
    print(key)
    df_dict[key] = df[:][df.STATION == key]


    station_df = df_dict[key].drop_duplicates(subset=['DateTime'])
    station_df = station_df.set_index('DateTime')
    station_df = station_df.reindex(pd.date_range(start='5/1/2018',end='4/8/2020',freq='5T'))
    station_df = station_df.iloc[12:]
    print(station_df.isnull().sum())
    
    station_df = station_df.apply(pd.to_numeric, errors='coerce')
    
    station_df = station_df.interpolate(method ='linear', limit_direction ='forward')
    
    print(station_df.isnull().sum())
    print(len(station_df))
    station_df.to_csv(str(key)+'.csv')