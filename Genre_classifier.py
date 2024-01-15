# -*- coding: utf-8 -*-
"""
Created on Sat Jan 13 15:10:48 2024

@author: yuyue
"""
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import classification_report
from sklearn.preprocessing import StandardScaler
from sklearn.multiclass import OneVsRestClassifier
from sklearn.preprocessing import MultiLabelBinarizer

# Load data
df = pd.read_csv(r"C:\Semester3YYYY\DataLiteracy\archive\cleaned_dataset2023.csv")

# Features
X = df[['Rank', 'Popularity', 'Favorites', 'Weighted_Score', 'Members']]

# Preprocess the 'Genres' column for multi-label classification
genres_list = df['Genres'].apply(lambda x: x.split(', '))
mlb = MultiLabelBinarizer()
y = mlb.fit_transform(genres_list)

# Standardize features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Build SVM model for multi-label classification
model = OneVsRestClassifier(SVC(kernel='rbf', gamma='scale', C=100))

# Train the model
model.fit(X_train, y_train)

# Prediction
predictions = model.predict(X_test)

# Evaluation
result = classification_report(y_test, predictions, zero_division=0, target_names=mlb.classes_)

predicted_genres = mlb.inverse_transform(predictions)
flat_predicted_genres = [genre for genres_tuple in predicted_genres for genre in genres_tuple]
print("Flat Predicted Genres:", flat_predicted_genres)

from collections import Counter

# List of predicted genres
predicted_genres = ['Comedy', 'Comedy', 'Comedy', 'Action', 'Adventure', 'Comedy', ...]

# Use Counter to count occurrences
genre_counts = Counter(predicted_genres)

# Find the most common genre
most_common_genre = genre_counts.most_common(1)[0][0]

print("Most Popular Genre:", most_common_genre)

from wordcloud import WordCloud
import matplotlib.pyplot as plt

# List of predicted genres
predicted_genres = ['Comedy', 'Comedy', 'Comedy', 'Action', 'Adventure', 'Comedy', 'Action', 'Action', 'Comedy', 'Comedy', 'Comedy', 'Action', 'Comedy', 'Comedy', 'Comedy', 'Action', 'Drama', 'Comedy', 'Comedy', 'Comedy', 'Action', 'Comedy', 'Comedy', 'Comedy', 'Comedy', 'Action', 'Comedy', 'Action', 'Comedy', 'Comedy', 'Comedy', 'Adventure', 'Action', 'Comedy', 'Comedy', 'Comedy', 'Comedy', 'Action', 'Action', 'Adventure', 'Action', 'Comedy', 'Comedy', 'Comedy', 'Romance', 'Comedy', 'Comedy', 'Action', 'Action', 'Fantasy', 'Comedy', 'Comedy', 'Action', 'Comedy', 'Drama', 'Action', 'Comedy', 'Comedy', 'Comedy', 'Action', 'Action', 'Comedy', 'Action', 'Drama', 'Comedy', 'Comedy', 'Comedy', 'Comedy', 'Adventure', 'Action', 'Action', 'Fantasy', 'Adventure', 'Comedy', 'Comedy', 'Action', 'Action', 'Action', 'Drama', 'Romance', 'Comedy', 'Action', 'Comedy', 'Comedy', 'Action', 'Comedy', 'Comedy', 'Comedy', 'Comedy', 'Comedy', 'Comedy', 'Comedy', 'Action', 'Comedy', 'Comedy', 'Comedy', 'Comedy', 'Romance', 'Comedy', 'Comedy', 'Comedy', 'Comedy', 'Comedy', 'Comedy', 'Romance', 'Comedy', 'Comedy', 'Comedy', 'Action', 'Comedy', 'Comedy', 'Romance', 'Comedy', 'Action', 'Fantasy', 'Horror', 'Comedy', 'Action', 'Action', 'Comedy', 'Comedy', 'Comedy', 'Action', 'Comedy', 'Comedy', 'Comedy', 'Comedy', 'Comedy', 'Comedy', 'Comedy', 'Adventure', 'Comedy', 'Comedy', 'Comedy', 'Comedy', 'Comedy', 'Comedy', 'Action', 'Horror', 'Comedy', 'Action', 'Comedy', 'Comedy', 'Romance', 'Comedy', 'Adventure', 'Comedy', 'Comedy', 'Comedy']

# Join the genres into a single string
text = ' '.join(predicted_genres)

# Create a WordCloud object
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)

# Display the WordCloud using matplotlib
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()
