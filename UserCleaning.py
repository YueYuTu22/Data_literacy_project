# -*- coding: utf-8 -*-
"""
Created on Wed Nov 22 13:31:25 2023

@author: yuyue
"""
import pandas as pd
import re
import json
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
#from statsmodels.multivariate.manova import MANOVA

# Replace 'your_file.csv' with the path to your CSV file
file_path = r'archive\users-details-2023.csv'

# Read the CSV file into a DataFrame
    
user_df = pd.read_csv(file_path, encoding='ISO-8859-1')

user_df = user_df.dropna()

user_df = user_df.iloc[:9000]

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

column_name6 = 'On Hold'
user_df = user_df.drop(column_name6, axis=1)

column_name7 = 'Rewatched'
user_df = user_df.drop(column_name7, axis=1)

column_name8 = 'Plan to Watch'
user_df = user_df.drop(column_name8, axis=1)

column_name8 = 'Watching'
user_df = user_df.drop(column_name8, axis=1)

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

#maov = MANOVA.from_formula('Days_Watched + Completed + Total_Entries + Episodes_Watched ~ Group', data=user_df)
#print(maov.mv_test())

X = user_df[['Days Watched', 'Completed', 'Total Entries','Episodes Watched']]
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

pca = PCA()
pca.fit(X_scaled)

explained_variance = pca.explained_variance_ratio_

loadings = pca.components_

(explained_variance, loadings)

print(loadings)

weights = loadings[0]

features = user_df[['Days Watched', 'Completed', 'Total Entries', 'Episodes Watched']]

user_df['Weighted_Y'] = (features * weights).sum(axis=1)

output = r'archive\cleaned_userdata.csv'

user_df.to_csv(output, index=False)