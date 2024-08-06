#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd

# Load data
df_rev = pd.read_csv(".data/REVBUS.csv")

# Define new order and filter out unwanted descriptions in one line
# Use copy() to avoid SettingWithCopyWarning when modifying this new DataFrame
df_rev = df_rev[
    ["Date started (UTC)", "Description", "Reference", "Balance", "Fee currency"]
].copy()
filtered_rev = df_rev[~df_rev["Description"].str.contains(r"Mihnea|RON")].copy()
# In[2]:

# Rename columns and add new column simultaneously, doing this safely using loc
filtered_rev.rename(
    columns={
        "Date started (UTC)": "Payment Date",
        "Description": "Merchant",
        "Reference": "Description",
        "Balance": "Debit",
        "Fee currency": "Currency",
    },
    inplace=True,
)
filtered_rev.loc[:, "Account"] = "Rev Business"

# In[3]:

# Convert dates efficiently and sort; ensure format matches your data
# Assuming date format in your CSV is year-month-day
filtered_rev["Payment Date"] = pd.to_datetime(
    filtered_rev["Payment Date"], format="%Y-%m-%d"
)
filtered_rev.sort_values("Payment Date", ascending=True, inplace=True)

# In[4]:

# Display the head of the DataFrame to check
print(filtered_rev.head())

# Save to CSV
filtered_rev.to_csv(".data/filtered_revbus.csv", index=False)
