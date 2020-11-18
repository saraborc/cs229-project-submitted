#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  7 18:27:38 2020

@author: saraborchers
"""
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
from sklearn.linear_model import SGDRegressor
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
figure(num=None, figsize=(18, 6), dpi=80, facecolor='w', edgecolor='k')

# Import training and validation datasets
X_matrix = np.genfromtxt('matrices/X_matrix_fc.csv', delimiter = ',')[:,1:]
y_vec = np.genfromtxt('matrices/y_vec_fc.csv', delimiter = ',')

# Train set is from 5/2/18 0:00 to 5/2/19 0:00. Index 0 - 105,120
X_train = X_matrix[:105120]
y_train = y_vec[:105120]

# Validation and test sets randomly sampled from 5/2/19 0:00 to 4/7/20 23:55. Index 105,120 - 203615
X_vt = X_matrix[105120:]
y_vt = y_vec[105120:]
X_valid, X_test, y_valid, y_test = train_test_split(X_vt, y_vt, test_size = 0.50, random_state=1)

# Find the optimal structure for a linear regressor
mse_min = 1
r2_max = 0
for lr in ['constant','optimal','invscaling','adaptive']:
    for p in ['l2','l1','elasticnet']:
        for l in ['squared_loss','huber','epsilon_insensitive','squared_epsilon_insensitive']:
            reg = make_pipeline(StandardScaler(), SGDRegressor(max_iter=1000, tol=1e-5, learning_rate = lr, penalty = p, loss = l)).fit(X_train,y_train)
            reg_y_pred = reg.predict(X_valid)
            mse = mean_squared_error(y_valid, reg_y_pred)
            r2 = r2_score(y_valid, reg_y_pred)
            if mse<mse_min and r2>r2_max:
                mse_min = mse
                r2_max = r2
                winner = lr+p+l

linreg = make_pipeline(StandardScaler(), SGDRegressor(max_iter=1000, tol=1e-5, learning_rate = 'constant', penalty = 'l1', loss = 'huber')).fit(X_train,y_train)
linreg_y_pred = reg.predict(X_valid)

print('Linreg Mean squared error: %.6f' % mean_squared_error(y_valid, linreg_y_pred))
print('Linreg Coefficient of determination: %.2f' % r2_score(y_valid, linreg_y_pred))

# Plot over one day
t = np.arange('2019-05-02 00:00','2019-05-03 00:00',np.timedelta64(10,'m'),dtype='datetime64')

# Uncomment to plot the MSE vs deviation from mean
mse_lr = np.square(linreg_y_pred-y_valid)
dev_actual = np.abs(y_valid - np.mean(y_valid))
plt.plot(t, mse_lr[:t.shape[0]], color = 'blue', label = "MSE Error")
plt.plot(t, dev_actual[:t.shape[0]], color = 'red', label = "Actual Deviation from Mean")

# # Uncomment to plot the predicted vs actual outputs
# plt.plot(t, reg_y_pred[:t.shape[0]], color = 'blue', label = "Lin Reg")
# plt.plot(t, y_valid[:t.shape[0]], color = 'red', label = "Actual")
# plt.xlabel("Date and Time")
# plt.ylabel("Carbon Emissions Intensity (mtCO2e/MWh)")

plt.xticks(rotation=45)
plt.legend()
plt.show()

