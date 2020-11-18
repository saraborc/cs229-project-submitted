#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 13 13:35:24 2020

@author: saraborchers
"""
import pandas as pd

# Create date ranges
idx = pd.date_range(start= '2018-05-02 00:00:00', end='2020-04-07 23:55:00', freq='5T')
idx2 = pd.date_range(start= '2018-05-02 00:00:00+00:00', end='2020-04-07 23:55:00+00:00', freq='5T')

# Import raw data files
co2 = pd.read_csv('../CO2 Rates/CO2-per-resource-04.2018-04.2020.csv')
supply = pd.read_csv('../Supply Data/supply-all-05.2018-05.20.csv')
wp = pd.read_csv('../weather_and_price.csv')
load = pd.read_csv('../Load Data/combined_load.csv')
load.rename(columns={'timestamp':'Datetime'}, inplace=True)
sac = pd.read_csv('../Weather Data/72483993225.csv')
sac.rename(columns={'Unnamed: 0':'Datetime'}, inplace=True)

# Start on May 2, 2018 and end on April 7, 2020
dates_dict = {0:[6140,-1152],1:[288,-6624],2:[6336,-217],3:[203,-15037],4:[276,-1]}
df_list = [co2, supply, wp, load, sac]

# Clean the data and interpolate as needed
for count,df in enumerate(df_list):
    df['Datetime'] = pd.to_datetime(df['Datetime'])
    df = df.set_index('Datetime').sort_index(axis=0)
    df = df.iloc[dates_dict[count][0]:dates_dict[count][1]]
    df = df[~df.index.duplicated(keep='first')]
    if count ==3:
        df = df.reindex(idx2)
    else:
        df = df.reindex(idx)
    df = df.interpolate()
    # df.reset_index(drop=True, inplace=True)
    df_list[count] = df
    
# Clean and create X matrix
df_list[3] = df_list[3].drop(columns=['Unnamed: 0'])
df_list[4] = df_list[4].drop(columns=['STATION'])
X_matrix = pd.concat([df_list[2].reset_index(drop=True),df_list[3].reset_index(drop=True),df_list[4].reset_index(drop=True)],axis=1)
X_matrix = X_matrix.set_index(idx)
X_matrix.to_csv('X_matrix_fc.csv',index=True, header=False)

# Calculate output vector
y_vec = df_list[0]['Natural gas'].add(df_list[0]['Imports'].add(df_list[0]['Coal']))
y_vec = y_vec.divide(df_list[1].sum(axis=1))
y_vec.to_csv('y_vec_fc.csv',index=False,header=False)

# Uncomment to plot histograms of select features
X_matrix = X_matrix.rename(columns={'UCD_DAM_Rate':'Electricity Price', 'windSpeedS2':'Wind Speed', 'windGustS2':'Wind Gust',
       'windBearingW2': 'Wind Bearing', 'load_MW': 'Load',
       'HourlyDryBulbTemperature':'Dry Temperature', 'HourlyRelativeHumidity':'Humidity',})
for c in ['Electricity Price', 'Wind Speed', 'Wind Gust','Wind Bearing', 'Load','Dry Temperature', 'Humidity']:
    
    ax = X_matrix.hist(column=c, bins=25, grid=False, figsize=(12,8), color='#86bf91', zorder=2, rwidth=0.9)
    
    ax = ax[0]
    for x in ax:
    
        # Despine
        x.spines['right'].set_visible(False)
        x.spines['top'].set_visible(False)
        x.spines['left'].set_visible(False)
    
        # Switch off ticks
        x.tick_params(axis="both", which="both", bottom="off", top="off", labelbottom="on", left="off", right="off", labelleft="on")
    
        # Draw horizontal axis lines
        vals = x.get_yticks()
        for tick in vals:
            x.axhline(y=tick, linestyle='dashed', alpha=0.4, color='#eeeeee', zorder=1)
    
        x.set_ylim()
        # Remove title
        x.set_title("")
    
        # Set x-axis label
        x.set_xlabel(c, labelpad=20, weight='bold', size=36)
    
        # Set y-axis label
        x.set_ylabel("Number of Samples", labelpad=20, weight='bold', size=36)


