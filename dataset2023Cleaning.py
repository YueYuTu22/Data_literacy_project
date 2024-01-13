# -*- coding: utf-8 -*-
"""
Created on Wed Nov 22 13:11:03 2023

@author: yuyue
"""
import numpy as np
import pandas as pd

# Replace 'your_file.csv' with the path to your CSV file
file_path = r'anime-dataset-2023.csv'

# Read the CSV file into a DataFrame
df = pd.read_csv(file_path)

# Drop rows with missing values in any column
df = df.dropna()

# Specify columns to drop
columns_to_drop = ['Image URL', 'Status', 'Other name', 'Aired', 'anime_id', 'Name',
                   'Source', 'Duration', 'Rating', 'Synopsis', 'Episodes', 'Licensors']

# Drop specified columns
df = df.drop(columns=columns_to_drop, axis=1)

# Replace 'UNKNOWN' values with NaN only in numerical columns
numerical_columns = df.select_dtypes(include=[np.number]).columns
df[numerical_columns] = df[numerical_columns].replace('UNKNOWN', pd.NA)

# Drop rows with NaN values
df = df.dropna()

# Handle 'UNKNOWN' values in non-numerical columns
non_numerical_columns = df.select_dtypes(exclude=[np.number]).columns
df[non_numerical_columns] = df[non_numerical_columns].replace('UNKNOWN', np.nan)

# Drop rows with NaN values
df = df.dropna()

# Convert 'Rank', 'Score', and 'Scored By' columns to numeric, handling errors by coercing to NaN
df['Rank'] = pd.to_numeric(df['Rank'], errors='coerce')
df['Score'] = pd.to_numeric(df['Score'], errors='coerce')
df['Scored By'] = pd.to_numeric(df['Scored By'], errors='coerce')

# Calculate Weighted Score
df['Weighted_Score'] = np.log1p(df['Score'] * df['Scored By'])

# Normalize 'Weighted_Score' to the range (1, 100)
df['Weighted_Score'] = np.interp(df['Weighted_Score'], (df['Weighted_Score'].min(), df['Weighted_Score'].max()), (1, 100))

# Reset index
df = df.reset_index(drop=True)

# Function to extract the season and year from the premiered string
def extract_season_year(premiered):
    if premiered == 'UNKNOWN':
        return None, None
    else:
        season, year = premiered.split()
        return season, int(year)

# Apply the function to extract the season and year from the "Premiered" column
season_year = df['Premiered'].map(extract_season_year)
df['Premiered Season'] = season_year.apply(lambda x: x[0])
df['Premiered Year'] = season_year.apply(lambda x: x[1])

# Drop the original 'Premiered' column
df.drop('Premiered', axis=1, inplace=True)

# Save the cleaned dataset to a new CSV file
output_path = r'cleaned_dataset2023.csv'
df.to_csv(output_path, index=False)
