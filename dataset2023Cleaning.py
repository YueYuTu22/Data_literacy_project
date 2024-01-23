# -*- coding: utf-8 -*-
"""
Created on Wed Nov 22 13:11:03 2023

@author: yuyue
"""

#
import numpy as np
import pandas as pd

# Replace 'your_file.csv' with the path to your CSV file
file_path = r'anime-dataset-2023.csv'

# Read the CSV file into a DataFrame
df1 = pd.read_csv(file_path)

# Drop rows with missing values in any column
df1 = df1.dropna()

# Specify columns to drop
columns_to_drop = ['Image URL', 'Status', 'Other name', 'Aired', 'anime_id', 'Name',
                   'Source', 'Duration', 'Rating', 'Synopsis', 'Episodes', 'Licensors', 'Premiered']

# Drop specified columns
df1 = df1.drop(columns=columns_to_drop, axis=1)

# Replace 'UNKNOWN' values with NaN only in numerical columns
numerical_columns = df1.select_dtypes(include=[np.number]).columns
df1[numerical_columns] = df1[numerical_columns].replace('UNKNOWN', pd.NA)

# Drop rows with NaN values
df1 = df1.dropna()

# Handle 'UNKNOWN' values in non-numerical columns
non_numerical_columns = df1.select_dtypes(exclude=[np.number]).columns
df1[non_numerical_columns] = df1[non_numerical_columns].replace('UNKNOWN', np.nan)


# Convert 'Rank', 'Score', and 'Scored By' columns to numeric, handling errors by coercing to NaN
df1['Rank'] = pd.to_numeric(df1['Rank'], errors='coerce')
df1['Score'] = pd.to_numeric(df1['Score'], errors='coerce')
df1['Scored By'] = pd.to_numeric(df1['Scored By'], errors='coerce')

# Calculate Weighted Score
df1['Weighted_Score'] = np.log1p(df1['Score'] * df1['Scored By'])

# Normalize 'Weighted_Score' to the range (1, 100)
df1['Weighted_Score'] = np.interp(df1['Weighted_Score'], (df1['Weighted_Score'].min(), df1['Weighted_Score'].max()), (1, 100))

# Reset index
df1 = df1.reset_index(drop=True)

df1 = df1.dropna()

# Save the cleaned dataset to a new CSV file
output_path = r'cleaned_dataset2023.csv'
df1.to_csv(output_path, index=False)
