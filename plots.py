# -*- coding: utf-8 -*-
"""
Created on Tue Jan  9 23:54:59 2024

@author: madhavi
"""

import pandas as pd
import matplotlib.pyplot as plt

file_path = r'cleaned_dataset2023.csv'

df = pd.read_csv(file_path)

studio_counts = df['Studios'].value_counts()

# Function to extract the season and year from the premiered string
def extract_season_year(premiered):
    if premiered == 'UNKNOWN':
        return None, None
    else:
        season, year = premiered.split()
        return season, int(year)

# Apply the function to extract the season and year from the "Premiered" column
season_year = df['Premiered'].map(extract_season_year)
df['Premiered Season'] = season_year.apply(lambda x: x[0])
df['Premiered Year'] = season_year.apply(lambda x: x[1])

# Drop the original 'Premiered' column
df.drop('Premiered', axis=1, inplace=True)

# Filter out anime titles with popularity value 0
df_valid_popularity = df[df['Popularity'] > 0]

selected_studio = 'Madhouse'  # Replace with the desired studio name
studio_data = df[df['Studios'] == selected_studio]

release_pattern = studio_data.groupby('Premiered Year')['English name'].count()

plt.figure(figsize=(10, 6))
plt.plot(release_pattern.index, release_pattern.values, marker='o', linestyle='-', color='b')
plt.title(f'Release Pattern of Animes for {selected_studio}')
plt.xlabel('Year')
plt.ylabel('Number of Animes Released')
plt.grid(True)
plt.show()

top_20_popular = df_valid_popularity.sort_values(by='Popularity', ascending=True).head(20)

from tabulate import tabulate

# Select specific rows and columns
selected_columns = ['English name','Producers', 'Studios', 'Premiered Year','Premiered Season', 'Popularity', 'Weighted_Score']

# Print the DataFrame as a table using tabulate
table_str = tabulate(top_20_popular[selected_columns], headers='keys', tablefmt='pretty')

# Print the table
print(table_str)

# Get the top 20 studios
top_studios = top_20_popular['Studios'].value_counts().index[:20]

# Plot the release pattern for each studio
plt.figure(figsize=(12, 8))

for selected_studio in top_studios:
    studio_data = df[df['Studios'] == selected_studio]
    release_pattern = studio_data.groupby('Premiered Year')['English name'].count()
    
    plt.plot(release_pattern.index, release_pattern.values, label=selected_studio, linestyle='-')

plt.title('Release Pattern of Top 20 Animes by Studios')
plt.xlabel('Year')
plt.ylabel('Number of Animes Released')
plt.legend()
plt.grid(True)
plt.show()

import seaborn as sns

# Get the top 20 studios
top_studios = top_20_popular['Studios'].value_counts().index[:20]

# Filter df to include only rows from top studios
df_top_studios = df[df['Studios'].isin(top_studios)]

# Create a pivot table for the heatmap
heatmap_data = pd.pivot_table(df_top_studios, values='English name', index='Studios', columns='Premiered Year', aggfunc='count', fill_value=0)

# Plot the heatmap
plt.figure(figsize=(15, 10))
sns.heatmap(heatmap_data, cmap='viridis', annot=True, fmt='g', linewidths=.5, cbar_kws={'label': 'Number of Animes Released'})

plt.title('Release Pattern of Top Studios (from df)')
plt.xlabel('Year')
plt.ylabel('Studio')
plt.show()

# Create a pivot table for the heatmap
heatmap_data = pd.crosstab(df_top_studios['Studios'], df_top_studios['Premiered Season'])

# Normalize the data to show percentages
heatmap_data_percent = heatmap_data.div(heatmap_data.sum(axis=1), axis=0) * 100

# Plot the heatmap
plt.figure(figsize=(12, 8))
sns.heatmap(heatmap_data_percent, cmap='viridis', annot=True, fmt='.2f', linewidths=.5)
plt.title('Season of Release for Top 20 Studios')
plt.xlabel('Season')
plt.ylabel('Studio')
plt.show()


# Calculate the total number of releases for each studio
release_counts = df_top_studios['Studios'].value_counts()

# Calculate the mean popularity score for each studio
popularity_means = df_top_studios.groupby('Studios')['Weighted_Score'].mean()

# Create a DataFrame with release counts and popularity means
correlation_data = pd.DataFrame({'Release_Count': release_counts, 'Weighted_Score_Mean': popularity_means})

# Create a scatter plot
plt.figure(figsize=(10, 6))
sns.scatterplot(x='Release_Count', y='Weighted_Score_Mean', data=correlation_data, hue=correlation_data.index, palette='viridis', s=100)

plt.title('Scatter Plot of Releases vs Popularity for Top 20 Studios')
plt.xlabel('Number of Releases')
plt.ylabel('Mean Weighted Score')
plt.legend(title='Studio', bbox_to_anchor=(1, 1))
plt.show()

