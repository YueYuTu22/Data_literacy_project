# -*- coding: utf-8 -*-
"""
Created on Sat Jan 13 13:29:44 2024

@author: madha
"""

import numpy as np
import pandas as pd

# Replace 'your_file.csv' with the path to your CSV file
file_path = r'/archive/rawData/anime-dataset-2023.csv'

# Read the CSV file into a DataFrame
df2 = pd.read_csv(file_path)

# Drop rows with missing values in any column
df2 = df2.dropna()

# Specify columns to drop
columns_to_drop = ['Image URL', 'Status', 'Other name', 'Premiered' , 'anime_id', 'Name',
                   'Source', 'Duration', 'Rating', 'Synopsis', 'Episodes', 'Licensors']

# Drop specified columns
df2 = df2.drop(columns=columns_to_drop, axis=1)

# Convert 'Rank', 'Score', and 'Scored By' columns to numeric, handling errors by coercing to NaN
df2['Rank'] = pd.to_numeric(df2['Rank'], errors='coerce')
df2['Score'] = pd.to_numeric(df2['Score'], errors='coerce')
df2['Scored By'] = pd.to_numeric(df2['Scored By'], errors='coerce')

# Calculate Weighted Score
df2['Weighted_Score'] = np.log1p(df2['Score'] * df2['Scored By'])

# Normalize 'Weighted_Score' to the range (1, 100)
df2['Weighted_Score'] = np.interp(df2['Weighted_Score'], (df2['Weighted_Score'].min(), df2['Weighted_Score'].max()), (1, 100))

# Replace 'UNKNOWN' values with NaN only in numerical columns
numerical_columns = df2.select_dtypes(include=[np.number]).columns
df2[numerical_columns] = df2[numerical_columns].replace('UNKNOWN', pd.NA)

# Drop rows with NaN values
df2 = df2.dropna()


# Reset index
df2 = df2.reset_index(drop=True)

def get_season(month):
    if month in ['Nov', 'Dec', 'Jan']:
        return 'Winter'
    elif month in ['Feb', 'Mar', 'Apr']:
        return 'Spring'
    elif month in ['May', 'Jun', 'Jul']:
        return 'Summer'
    elif month in ['Aug', 'Sep', 'Oct']:
        return 'Fall'
    else:
        return 'UNKNOWN'
    
df2['Aired_Year'] = df2['Aired'].str.extract(r'\b(\d{4})\b')
df2['Start Month'] = df2['Aired'].str.split().str[0]
df2['Season'] = df2['Start Month'].apply(get_season)

import pandas as pd

# Assuming df is your DataFrame
df2 = df2[(df2['Genres'] != 'UNKNOWN') & (df2['Season'] != 'UNKNOWN')]


# Save the cleaned dataset to a new CSV file
output_path = r'cleaned_dataset2023_unknown.csv'
df2.to_csv(output_path, index=False)
