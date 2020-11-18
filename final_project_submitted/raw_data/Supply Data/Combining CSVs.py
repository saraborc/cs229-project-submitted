#!/usr/bin/env python
# coding: utf-8

# In[2]:


import os
import glob
import pandas as pd
import datetime as dt


# In[3]:


extension = 'csv'

all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
#combine all files in the list
# for f in all_filenames:
#     df = (pd.read_csv(f,header=None,skiprows=0).T)
#     print('pause')
combined_csv = pd.concat([pd.read_csv(f).T for f in all_filenames ], sort=True)
#export to csv
# combined_csv.to_csv( "combined_csv.csv", index=False, encoding='utf-8-sig')
# df = pd.read_csv(all_filenames[0])
#df_all.index = df_all['Time stamp']
#pd.to_datetime(df_all.index)
#df_all.drop(columns=['Time stamp'], inplace = True)
#df_all.index = pd.DatetimeIndex(df_all.index)
#df_all = df_all.resample('H').mean()
#for f in all_filenames: 
#    val = f.split(' ')
#    col_name = val[0]
#    print(col_name)
#    df_new = pd.read_csv(f, thousands=',')
#    df_new.index = df_new['Time stamp']
#    df_new.index = pd.DatetimeIndex(df_new.index)
#    df_new = df_new.filter(['Value'])
#    df_new['Value'] = pd.to_numeric(df_new['Value'], downcast = 'float')
#    
#    df_new = df_new.resample('H').mean()
#    df_new.rename(columns={'Value': col_name}, inplace = True)
#    df_all = pd.concat([df_all, df_new], axis = 1, sort = False)
#    
#df_all.to_excel('All_Data_090120202.xlsx')
#


# In[4]:


# df.head()


# In[ ]:




