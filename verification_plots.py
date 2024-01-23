# -*- coding: utf-8 -*-
"""
Created on Tue Jan 23 09:30:16 2024

@author: madha
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import MultiLabelBinarizer

# Planned plots:
#   World map: Gender distribution
#   Top 20 anime vs Studios
#   Heat map: Season vs Studios
#   Genre vs Studios
#   Type vs Studios

# World map: Done by Ruitong

# Data Cleaning to get Top 20 anime and their studios:
file_path = r'cleaned_dataset2023_unknown.csv'
df = pd.read_csv(file_path)
df_valid_popularity = df[df['Popularity'] > 0]
top_20_popular = df_valid_popularity.sort_values(by='Popularity', ascending=True).head(20)
top_studios = top_20_popular['Studios'].value_counts().index[:20]
# Filter the DataFrame to include only the top studios (for top 20)
top_studios_df = top_20_popular[top_20_popular['Studios'].isin(top_studios)]
# Filter df to include only rows from top studios (for all anime)
top_studios_all = df[df['Studios'].isin(top_studios)]


# Top 20 anime vs studio
plt.figure(figsize=(12, 8))
sns.countplot(y='Studios', data=top_studios_df, order=top_studios_df['Studios'].value_counts().index, palette='viridis')
plt.xlabel('Number of Anime present in top 20')
plt.ylabel('Studios')
plt.title('Studios that Released the Top 20 Animes')
plt.show()

# Calculate the total number of releases for each studio
release_counts = top_studios_all['Studios'].value_counts()

# Calculate the mean popularity score for each studio
popularity_means = top_studios_all.groupby('Studios')['Weighted_Score'].mean()

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


# Studios vs season
# Create a pivot table for the heatmap
heatmap_data = pd.crosstab(top_studios_all['Studios'], top_studios_all['Season'])

# Normalize the data to show percentages
heatmap_data_percent = heatmap_data.div(heatmap_data.sum(axis=1), axis=0) * 100

# Plot the heatmap
plt.figure(figsize=(12, 8))
sns.heatmap(heatmap_data_percent, cmap='viridis')
plt.title('Season of Airing for Top Studios')
plt.xlabel('Season')
plt.ylabel('Studio')
plt.show()


# Studios vs Genres
# Combine the two DataFrames to include all relevant rows
df_genres_studios = pd.concat([top_studios_df, top_studios_all])
# Reset the index to ensure it is unique
df_genres_studios = df_genres_studios.reset_index(drop=True)
# Filter the DataFrame to include only the rows with non-UNKNOWN genres
df_genres_studios = df_genres_studios[df_genres_studios['Genres'] != 'UNKNOWN']
# Preprocess the 'Genres' column for multi-label classification
genres_list = df_genres_studios['Genres'].apply(lambda x: x.split(', '))
mlb = MultiLabelBinarizer()
y_genres = mlb.fit_transform(genres_list)
# Add the 'Genres' information to the DataFrame
df_genres_studios = pd.concat([df_genres_studios, pd.DataFrame(y_genres, columns=mlb.classes_)], axis=1)
# Group by studios and sum the counts of each genre
grouped_df = df_genres_studios.groupby('Studios')[mlb.classes_].sum()
# Plotting a stacked bar plot
plt.figure(figsize=(15, 8))
grouped_df.plot(kind='bar', stacked=True, colormap='viridis')
plt.xlabel('Studios')
plt.ylabel('Count')
plt.title('Genres vs Top Studios')
plt.legend(title='Genres', bbox_to_anchor=(1.05, 1), loc='upper left')  # Move legend outside the plot
plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better visibility
plt.show()


# Type vs Studios 
# Filter the DataFrame to include only the rows with top studios
df_studios_types = df_valid_popularity[df_valid_popularity['Studios'].isin(top_studios)]
# Create a DataFrame with the count of each type for each studio
df_types_studios = pd.crosstab(df_studios_types['Studios'], df_studios_types['Type'])
# Plotting a grouped bar plot
plt.figure(figsize=(12, 8))
df_types_studios.plot(kind='bar', stacked=True, colormap='viridis')
plt.xlabel('Studios')
plt.ylabel('Count')
plt.title('Anime Types vs Top Studios')
plt.legend(title='Type', bbox_to_anchor=(1.05, 1), loc='upper left')  # Move legend outside the plot
plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better visibility
plt.show()






