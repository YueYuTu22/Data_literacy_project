# -*- coding: utf-8 -*-
"""
Created on Wed Nov 22 13:31:25 2023

@author: yuyue
"""
from geograpy import places
import pandas as pd
import re
import json

# Replace 'your_file.csv' with the path to your CSV file
file_path = r'archive\users-details-2023.csv'

# Read the CSV file into a DataFrame
    
user_df = pd.read_csv(file_path, encoding='ISO-8859-1')

user_df = user_df.dropna()

user_df = user_df.iloc[:4000]

column_name = 'Username'
user_df = user_df.drop(column_name, axis=1)

column_name2 = 'Mal ID'
user_df = user_df.drop(column_name2, axis=1)

column_name3 = 'Joined'
user_df = user_df.drop(column_name3, axis=1)

column_name4 = 'Mean Score'
user_df = user_df.drop(column_name4, axis=1)

column_name5 = 'Dropped'
user_df = user_df.drop(column_name5, axis=1)

location = 'Location'
user_df = user_df[user_df[location].map(lambda x: x.isascii())]
user_df[location] = user_df[location].str.replace(r'\W', '')
user_df = user_df[user_df[location].str.strip() != '']
mask = ~user_df[location].str.isnumeric()
user_df = user_df[mask]
user_df = user_df[~user_df[location].str.contains(r'\d', na=False)]

def clean_text(text):
    return text.encode('ascii', errors='ignore').decode('ascii')

user_df['Location'] = user_df['Location'].apply(clean_text)

with open('Mapping.json', 'r') as file:
    region_to_country = json.load(file)


def extract_country1(location): 
    for region, country in region_to_country.items():
        if region in location:
            return country
    
    return location

def extract_country2(location):
    match = re.search(r'[A-Z][a-z]+$', location)
    if match:
        return match.group()
    return location

user_df['Country'] = user_df['Location'].apply(extract_country2)


user_df['Country'] = user_df['Country'].apply(extract_country1)

birth = 'Birthday'
threshold_date = '1940-01-01'
user_df[birth] = pd.to_datetime(user_df[birth], errors='coerce')
threshold_date = pd.to_datetime(threshold_date).tz_localize('UTC')
# Create a boolean mask where 'birthday' is less than or equal to the threshold date
mask2 = (user_df[birth] >= pd.to_datetime(threshold_date))
# Apply the boolean mask to keep rows where 'birthday' is less than or equal to the threshold date
user_df = user_df[mask2]

user_df = user_df.reset_index(drop=True)

user_df_head = user_df.head(10)

# Display the first 10 rows of the DataFrame
print(user_df_head)

print(user_df['Location'].head(20))

column_names = user_df.columns
print(column_names)

output = r'archive\cleaned_userdata.csv'