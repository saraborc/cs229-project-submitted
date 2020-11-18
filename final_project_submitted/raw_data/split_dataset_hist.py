#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 23 15:40:05 2020

@author: saraborchers
"""
import pandas as pd
import os
from sklearn.model_selection import train_test_split

# Get the file from parent directory and read into df
filename = os.path.join(os.getcwd(),'..','final_dataset.csv')
df = pd.read_csv(filename,low_memory=False)

# Convert timestamp to type datetime
df['timestamp']=pd.to_datetime(df['timestamp'])
df = df.set_index('timestamp').sort_index(axis=0)
# df['timestamp']=pd.to_numeric(df['timestamp'])

# Fill in missing values for carbon intensity
df['carbon_intensity'] = df['carbon_intensity'].interpolate(method ='linear', limit_direction ='forward')

# Separate out the x and y vectors
df_X = df.drop(['carbon_intensity'],axis=1)
df_y = df['carbon_intensity']

# Uncomment to remove features with low values in covariance matrix
df_X_shortened = df.drop(['UCD_RTM_Rate','carbon_intensity',
       'LA - HourlyDryBulbTemperature', 'LA - HourlyRelativeHumidity',
       'LA - HourlyWetBulbTemperature', 'SD - HourlyDryBulbTemperature',
       'SD-HourlyRelativeHumidity', 'SD-HourlyWetBulbTemperature',
       'temperatureW2',
       'apparentTemperatureW2', 'humidityW2', 'windSpeedW2', 'windGustW2',
       'temperatureW4', 'apparentTemperatureW4', 'humidityW4',
       'windSpeedW4', 'windGustW4', 'windBearingW4', 'temperatureW3',
       'apparentTemperatureW3', 'humidityW3', 'windSpeedW3', 'windGustW3',
       'windBearingW3', 'visibilityW3', 'temperatureS1',
       'apparentTemperatureS1', 'humidityS1', 'windSpeedS1', 'windGustS1',
       'windBearingS1', 'uvIndexS1', 'temperatureW5', 'apparentTemperatureW5',
       'humidityW5', 'windSpeedW5', 'windGustW5',
       'cloudCoverW5', 'uvIndexW5', 'visibilityW5', 'temperatureS2',
       'apparentTemperatureS2', 'humidityS2', 'pressureS2',
       'windBearingS2', 'cloudCoverS2', 'uvIndexS2',
       'visibilityS2', 'temperatureS4', 'apparentTemperatureS4', 'humidityS4',
       'windSpeedS4', 'windGustS4', 'windBearingS4', 'uvIndexS4',
       'visibilityS4', 'temperatureW1', 'apparentTemperatureW1', 'humidityW1',
       'windSpeedW1', 'windGustW1', 'windBearingW1', 'cloudCoverW1',
       'uvIndexW1', 'visibilityW1', 'temperatureS3', 'apparentTemperatureS3',
       'humidityS3', 'pressureS3',
       'windBearingS3', 'cloudCoverS3', 'uvIndexS3', 'visibilityS3',
       'temperatureS5', 'apparentTemperatureS5', 'humidityS5', 'windSpeedS5',
       'windGustS5', 'windBearingS5', 'cloudCoverS5', 'uvIndexS5',
       'visibilityS5'],axis=1)


X_train, X_test, y_train, y_test = train_test_split(df_X, df_y, test_size=0.15, random_state=1)
X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.1765, random_state=1)

# Creates a csv for each vector, IGNORING the timestamp
X_train.drop(columns = ['timestamp']).sort_index(axis=0).to_csv('X_train.csv', header=False, index=False)
X_val.drop(columns = ['timestamp']).sort_index(axis=0).to_csv('X_valid.csv', header=False, index=False)
X_test.drop(columns = ['timestamp']).sort_index(axis=0).to_csv('X_test.csv', header=False, index=False)
y_train.drop(columns = ['timestamp']).sort_index(axis=0).to_csv('y_train.csv', header=False, index=False)
y_val.drop(columns = ['timestamp']).sort_index(axis=0).to_csv('y_valid.csv', header=False, index=False)
y_test.drop(columns = ['timestamp']).sort_index(axis=0).to_csv('y_test.csv', header=False, index=False)
