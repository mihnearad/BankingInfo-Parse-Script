#!/usr/bin/env python
# coding: utf-8

# In[9]:
import pandas as pd
import numpy as np

# Load data and assign currency
btradron = pd.read_csv("./.data/BTRADRON.csv", skiprows=16)
btradron["Currency"] = "RON"

btradeur = pd.read_csv("./.data/BTRADEUR.csv", skiprows=16)
btradeur["Currency"] = "EUR"

# Concatenate dataframes
df = pd.concat([btradron, btradeur], ignore_index=True)

# Drop unnecessary columns
df.drop(columns=["Referinta tranzactiei", "Credit", "Sold contabil", "Data valuta"], inplace=True)

print(df.head())

# In[11]:
# Extract and filter data
df["Payment Date"] = df["Descriere"].str.extract(r"(POS\s(\d{2}\/\d{2}\/\d{4}))")[1]
regex_pattern = r"Schimb valutar|LT383250069969855031|Comision"
filtered_df = df[~df["Descriere"].str.contains(regex_pattern)].copy()

# Convert and format dates
date_formats = ["%d/%m/%Y", "%Y-%m-%d", "%d-%m-%Y"]
for fmt in date_formats:
    filtered_df["Payment Date"] = pd.to_datetime(filtered_df["Payment Date"], format=fmt, errors="coerce")

filtered_df["Payment Date"].fillna(filtered_df["Data tranzactie"], inplace=True)
filtered_df["Data tranzactie"] = pd.to_datetime(df["Data tranzactie"], errors="coerce")

# Format dates to 'day-month-year'
filtered_df["Payment Date"] = filtered_df["Payment Date"].dt.strftime("%d-%m-%Y")
filtered_df["Data tranzactie"] = filtered_df["Data tranzactie"].dt.strftime("%d-%m-%Y")

print(filtered_df.head())

# In[12]:
# Extract merchant information
filtered_df["Merchant"] = filtered_df["Descriere"].str.extract(r"TID:\s*(?:[^\s]{2,8}\s+)?(\w+)")
filtered_df["Merchant"].fillna(df["Descriere"].str.split(";").str[3], inplace=True)

print(filtered_df.head())

# In[13]:
# Convert to datetime for sorting and format for output
filtered_df['Payment Date'] = pd.to_datetime(filtered_df['Payment Date'], errors='coerce', dayfirst=True)
filtered_df['Data tranzactie'] = pd.to_datetime(filtered_df['Data tranzactie'], errors='coerce', dayfirst=True)

# Sort the DataFrame by 'Payment Date'
filtered_df.sort_values(by='Payment Date', ascending=True, inplace=True)

# Rename and reorder columns
filtered_df = filtered_df.rename(
    columns={
        "Descriere": "Description",
        "Debit": "Debit",
        "Fee Currency": "Currency"
    }
)

filtered_df["Account"] = "BT Business"
new_column_order = ['Payment Date', 'Merchant', 'Description', 'Debit', 'Currency', 'Account']
filtered_df = filtered_df[new_column_order]

print(filtered_df.head())

# In[15]:
# Save to CSV
filtered_df.to_csv(".data/filtered_bt.csv", index=False)
