# -*- coding: utf-8 -*-
"""
Created on Wed Nov 22 13:11:03 2023

@author: yuyue
"""

import pandas as pd

# Replace 'your_file.csv' with the path to your CSV file
file_path = r'archive\anime-dataset-2023.csv'

# Read the CSV file into a DataFrame
df = pd.read_csv(file_path)

df = df.dropna()

column_name = 'Image URL'
df = df.drop(column_name, axis=1)

column_name2 = 'Status'
df = df.drop(column_name2, axis=1)

column_name3 = 'Other name'
df = df.drop(column_name3, axis=1)

column_name4 = 'Aired'
df = df.drop(column_name4, axis=1)

column_name5 = 'anime_id'
df = df.drop(column_name5, axis=1)

column_name6 = 'Name'
df = df.drop(column_name6, axis=1)

column_name7 = 'Premiered'
df = df.drop(column_name7, axis=1)

column_name8 = 'Source'
df = df.drop(column_name8, axis=1)

column_name8 = 'Duration'
df = df.drop(column_name8, axis=1)

column_name9 = 'Rating'
df = df.drop(column_name9, axis=1)

value_to_drop = 'UNKNOWN'

#mask = df['English name'] != value_to_drop
#df = df[mask]

#mask2 = df['Producers'] != value_to_drop
#df = df[mask2]

#mask3 = df['Genres'] != value_to_drop
#df = df[mask3]

df_replaced = df.replace('UNKNOWN', pd.NA)
df = df_replaced.dropna()

#df_head = df.head(5)
#column_names = df.columns
#print(column_names)
#print(df_head)

output = r'archive\cleaned_dataset2023.csv' # This is a path in the current writable directory

# Save the cleaned DataFrame to a CSV file
df.to_csv(output, index=False)

