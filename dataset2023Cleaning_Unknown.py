# -*- coding: utf-8 -*-
"""
Created on Sat Jan 13 13:29:44 2024

@author: madha
"""

import numpy as np
import pandas as pd

# Replace 'your_file.csv' with the path to your CSV file
file_path = r'anime-dataset-2023.csv'

# Read the CSV file into a DataFrame
df2 = pd.read_csv(file_path)

# Drop rows with missing values in any column
df2 = df2.dropna()

# Specify columns to drop
columns_to_drop = ['Image URL', 'Status', 'Other name', 'Aired', 'anime_id', 'Name',
                   'Source', 'Duration', 'Rating', 'Synopsis', 'Episodes', 'Licensors']

# Drop specified columns
df2 = df2.drop(columns=columns_to_drop, axis=1)

# Replace 'UNKNOWN' values with NaN only in numerical columns
numerical_columns = df2.select_dtypes(include=[np.number]).columns
df2[numerical_columns] = df2[numerical_columns].replace('UNKNOWN', pd.NA)

# Drop rows with NaN values
df2 = df2.dropna()

# Convert 'Rank', 'Score', and 'Scored By' columns to numeric, handling errors by coercing to NaN
df2['Rank'] = pd.to_numeric(df2['Rank'], errors='coerce')
df2['Score'] = pd.to_numeric(df2['Score'], errors='coerce')
df2['Scored By'] = pd.to_numeric(df2['Scored By'], errors='coerce')

# Calculate Weighted Score
df2['Weighted_Score'] = np.log1p(df2['Score'] * df2['Scored By'])

# Normalize 'Weighted_Score' to the range (1, 100)
df2['Weighted_Score'] = np.interp(df2['Weighted_Score'], (df2['Weighted_Score'].min(), df2['Weighted_Score'].max()), (1, 100))

# Reset index
df2 = df2.reset_index(drop=True)

# Function to extract the season and year from the premiered string
def extract_season_year(premiered):
    if premiered == 'UNKNOWN':
        return None, None
    else:
        season, year = premiered.split()
        return season, int(year)

# Apply the function to extract the season and year from the "Premiered" column
season_year = df2['Premiered'].map(extract_season_year)
df2['Premiered Season'] = season_year.apply(lambda x: x[0])
df2['Premiered Year'] = season_year.apply(lambda x: x[1])

# Drop the original 'Premiered' column
df2.drop('Premiered', axis=1, inplace=True)

# Save the cleaned dataset to a new CSV file
output_path = r'cleaned_dataset2023_unknown.csv'
df2.to_csv(output_path, index=False)
