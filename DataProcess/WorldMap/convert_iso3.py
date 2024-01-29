#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 15 14:01:52 2024

@author: ruitongliu
"""

import pandas as pd
import pycountry

# load csv file
csv_file = '/Users/ruitongliu/Desktop/Data_literacy_project/DataLiteracy/archive/cleaned_userdata.csv'  # 替换为您的CSV文件路径
df = pd.read_csv(csv_file)

def country_to_iso3(country_name):
    try:
        country = pycountry.countries.search_fuzzy(country_name)
        if country:
            return country[0].alpha_3
        else:
            return "Country not found"
    except LookupError:
        return "Invalid country name"

# add the new ISO3_Code into the new line
df['ISO3_Code'] = df['Country'].apply(country_to_iso3)

# save the file
output_csv_file = '/Users/ruitongliu/Desktop/Data_literacy_project/DataLiteracy/archive/iso3_output1.csv'  # 替换为输出的CSV文件路径
df.to_csv(output_csv_file, index=False)


