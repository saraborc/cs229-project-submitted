#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 15 09:29:36 2020

@author: saraborchers
"""
import pandas as pd
import os
from sklearn.model_selection import train_test_split

X = pd.read_csv('X_matrix_fc.csv',header = None,low_memory=False)
y = pd.read_csv('y_vec_fc.csv',header= None,low_memory=False)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15, random_state=1)
X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.1765, random_state=1)

# Creates a csv for each vector, IGNORING the timestamp
X_train.drop(X_train.columns[0],axis=1).sort_index(axis=0).to_csv('X_train_fc.csv', header=False, index=False)
X_val.drop(X_val.columns[0],axis=1).sort_index(axis=0).to_csv('X_val_fc.csv', header=False, index=False)
X_test.drop(X_test.columns[0],axis=1).sort_index(axis=0).to_csv('X_test_fc.csv', header=False, index=False)
y_train.sort_index(axis=0).to_csv('y_train_fc.csv', header=False, index=False)
y_val.sort_index(axis=0).to_csv('y_val_fc.csv', header=False, index=False)
y_test.sort_index(axis=0).to_csv('y_test_fc.csv', header=False, index=False)

