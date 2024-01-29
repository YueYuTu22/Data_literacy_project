#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 23 13:41:44 2024

@author: ruitongliu
"""

import pandas as pd
import plotly.express as px

# Load data
file_path ='/Users/ruitongliu/Desktop/Data_literacy_project/DataLiteracy/archive/iso3_output1.csv' # Replace with the path to your file
data = pd.read_csv(file_path)

# Filter out Antarctica based on its ISO alpha-3 code ('ATA')
data = data[data['ISO3_Code'] != 'ATA']

# Calculate the median of Weighted_Y for each country
median_weighted_y = data.groupby('ISO3_Code')['Weighted_Y'].median()

# Prepare data for plotting
plot_data = median_weighted_y.reset_index()
plot_data.columns = ['iso_alpha', 'Median of Weighted_Y']

# Create world map
fig = px.choropleth(plot_data, 
                    locations="iso_alpha",
                    color="Median of Weighted_Y",
                    hover_name="iso_alpha",
                    color_continuous_scale="Jet",
                    title="World Map of Median Weighted_Y",
                    projection="natural earth")
# Set country boundaries to black
fig.update_geos(showcountries=True, countrycolor="Black")

# Show the map
fig.show(renderer='browser')
