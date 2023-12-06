# -*- coding: utf-8 -*-
"""
Created on Wed Nov 22 13:31:25 2023

@author: yuyue
"""

import pandas as pd
import re

# Replace 'your_file.csv' with the path to your CSV file
file_path = r'C:\Semester3YYYY\DataLiteracy\archive\users-details-2023.csv'

# Read the CSV file into a DataFrame
user_df = pd.read_csv(file_path)

user_df = user_df.dropna()

column_name = 'Username'
user_df = user_df.drop(column_name, axis=1)

column_name2 = 'Mal ID'
user_df = user_df.drop(column_name2, axis=1)


location = 'Location'
user_df = user_df[user_df[location].map(lambda x: x.isascii())]
user_df[location] = user_df[location].str.replace(r'\W', '')
user_df = user_df[user_df[location].str.strip() != '']
mask = ~user_df[location].str.isnumeric()
user_df = user_df[mask]
user_df = user_df[~user_df[location].str.contains(r'\d', na=False)]


birth = 'Birthday'
threshold_date = '1940-01-01'
user_df[birth] = pd.to_datetime(user_df[birth], errors='coerce')
threshold_date = pd.to_datetime(threshold_date).tz_localize('UTC')
# Create a boolean mask where 'birthday' is less than or equal to the threshold date
mask2 = (user_df[birth] >= pd.to_datetime(threshold_date))
# Apply the boolean mask to keep rows where 'birthday' is less than or equal to the threshold date
user_df = user_df[mask2]

user_df_head = user_df.head(10)

# Display the first 10 rows of the DataFrame
print(user_df_head)

column_names = user_df.columns
print(column_names)