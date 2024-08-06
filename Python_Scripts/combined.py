#!/usr/bin/env python
# coding: utf-8

# In[17]:


import pandas as pd 
import numpy as np 

rev_bus = pd.read_csv('.data/filtered_revbus.csv')

bt = pd.read_csv('.data/filtered_bt.csv')

rev_pers = pd.read_csv('.data/filtered_revpers.csv')

transactions= pd.concat([rev_bus, bt, rev_pers], axis=0)



transactions.to_csv('.data/transactions.csv', index=False)

