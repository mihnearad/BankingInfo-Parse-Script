#!/usr/bin/env python
# coding: utf-8

# In[38]:
import pandas as pd
import numpy as np

# Load data from CSV files
revpers_ron = pd.read_csv("./.data/REVPERS.csv")
revpers_eur = pd.read_csv("./.data/REVPERS_EUR.csv")

# Concatenate data and set initial column values
revpers = pd.concat([revpers_ron, revpers_eur], ignore_index=True)
revpers["Account"] = "Rev Pers"
revpers["Description2"] = ""  # Adding empty column to match the other tables

print(revpers.head())

# In[41]:
# Apply regex to filter out rows and drop unnecessary columns
regex_pattern = r"INTEREST|EXCHANGE|DEPOSIT"
mask = ~revpers["Type"].str.contains(regex_pattern)
filtered_revpers = revpers.loc[mask].copy()

# Drop specified columns
filtered_revpers.drop(
    columns=["Balance", "State", "Fee", "Completed Date", "Product", "Type"],
    inplace=True,
)

# Rename columns to match expected output structure
filtered_revpers.rename(
    columns={
        "Started Date": "Payment Date",
        "Description": "Merchant",  # Assuming the original 'Description' should be 'Merchant'
        "Description2": "Description",  # 'Description2' is renamed to 'Description'
        "Amount": "Debit",
    },
    inplace=True,
)

# Specify new column order
new_order = ["Payment Date", "Merchant", "Description", "Debit", "Currency", "Account"]
filtered_revpers = filtered_revpers[new_order]

# Convert 'Payment Date' to a formatted date string
filtered_revpers["Payment Date"] = pd.to_datetime(
    filtered_revpers["Payment Date"]
).dt.strftime("%Y-%m-%d")

print(filtered_revpers.head())

# In[42]:
# Save the filtered DataFrame to CSV
filtered_revpers.to_csv("./.data/filtered_revpers.csv", index=False)
