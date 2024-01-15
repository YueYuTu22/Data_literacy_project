#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 15 14:01:52 2024

@author: ruitongliu
"""

import pandas as pd
import pycountry

# 读取CSV文件
csv_file = '/Users/ruitongliu/Desktop/Data_literacy_project/DataLiteracy/archive/cleaned_userdata.csv'  # 替换为您的CSV文件路径
df = pd.read_csv(csv_file)

# 定义将国家名称转换为ISO3代码的函数
def country_to_iso3(country_name):
    try:
        country = pycountry.countries.search_fuzzy(country_name)
        if country:
            return country[0].alpha_3
        else:
            return "Country not found"
    except LookupError:
        return "Invalid country name"

# 将Country列中的国家名称转换为ISO3代码并添加到新列
df['ISO3_Code'] = df['Country'].apply(country_to_iso3)

# 将结果保存到新的CSV文件
output_csv_file = '/Users/ruitongliu/Desktop/Data_literacy_project/DataLiteracy/archive/iso3_output1.csv'  # 替换为输出的CSV文件路径
df.to_csv(output_csv_file, index=False)


