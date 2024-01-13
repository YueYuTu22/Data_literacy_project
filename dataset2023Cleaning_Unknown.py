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

# Save the cleaned dataset to a new CSV file
output_path = r'cleaned_dataset2023_unknown.csv'
df.to_csv(output_path, index=False)
