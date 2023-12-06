# -*- coding: utf-8 -*-
"""
Created on Wed Nov 22 14:01:30 2023

@author: yuyue
"""

import pandas as pd
import re
# Replace 'your_file.csv' with the path to your CSV file
file_path = r'C:\Semester3YYYY\DataLiteracy\archive\users-score-2023.csv'

# Read the CSV file into a DataFrame
df = pd.read_csv(file_path)

df = df.dropna()

column_name = 'Username'
df = df.drop(column_name, axis=1)

# Assuming 'df' is your DataFrame
df_head = df.head(10)

# Display the first 10 rows of the DataFrame
print(df_head)


