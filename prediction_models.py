# -*- coding: utf-8 -*-
"""
Created on Tue Jan 23 09:07:51 2024

@author: madha
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
import numpy as np
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.preprocessing import StandardScaler
from sklearn.multiclass import OneVsRestClassifier
from sklearn.metrics import classification_report


# Importing data sets
# Season:
df_season = pd.read_csv('cleaned_dataset2023_unknown.csv')
# Type:
df_type = pd.read_csv('cleaned_dataset2023.csv')
# Genre
df = pd.read_csv("cleaned_dataset2023_unknown.csv")

# Remove rows with 'UNKNOWN' in 'Genres'
df = df[df['Genres'] != 'UNKNOWN']



# Convert categorical features to numerical labels
label_encoder_season = LabelEncoder()
label_encoder_type = LabelEncoder()

df_season['Season'] = label_encoder_season.fit_transform(df_season['Season'])
df_type['Type'] = label_encoder_type.fit_transform(df_type['Type'])

# Define features (X) and target variables (y)
X_season = df_season[['Popularity', 'Weighted_Score', 'Members', 'Favorites',]]
X_type = df_type[['Popularity', 'Weighted_Score', 'Members',  'Favorites',]]
X = df[['Popularity', 'Favorites', 'Weighted_Score', 'Members']]
y_season = df_season['Season']
y_type = df_type['Type']

# Preprocess the 'Genres' column for multi-label classification
genres_list = df['Genres'].apply(lambda x: x.split(', '))
mlb = MultiLabelBinarizer()
y = mlb.fit_transform(genres_list)

# Split the data into training and testing sets
X_train_season, X_test_season, y_train_season, y_test_season = train_test_split(
    X_season, y_season, test_size=0.2, random_state=42
)

X_train_type, X_test_type, y_train_type, y_test_type = train_test_split(
    X_type, y_type, test_size=0.2, random_state=42
)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Standardize features for Genres
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Build and train the conditional probability models
model_season = GaussianNB(var_smoothing=0.01)
model_season.fit(X_train_season , y_train_season)

model_type = GaussianNB()
model_type.fit(X_train_type, y_train_type)

classifier = OneVsRestClassifier(GaussianNB(var_smoothing=0.5))  # Adjust var_smoothing as needed
classifier.fit(X_train_scaled, y_train)

# Predictions on the test set
y_pred_prob_season = model_season.predict_proba(X_test_season )
y_pred_prob_type = model_type.predict_proba(X_test_type)
y_pred_prob = classifier.predict_proba(X_test_scaled)


# Find instances with the highest predicted probability
best_pred_idx_season = y_pred_prob_season.argmax(axis=1)
best_pred_idx_type = y_pred_prob_type.argmax(axis=1)
best_pred_idx_genre = y_pred_prob.argmax(axis=1)

# Display the best predictions for season and type
best_pred_season = label_encoder_season.inverse_transform(model_season.classes_[best_pred_idx_season])[0]
best_pred_type = label_encoder_type.inverse_transform(model_type.classes_[best_pred_idx_type])[0]
best_pred_idx_genre = mlb.classes_[best_pred_idx_genre]

print(f"Best Prediction for Season: {best_pred_season}")
print(f"Best Prediction for Type: {best_pred_type}")
print(f"Best Prediction for Genre: {best_pred_idx_genre[0]}")

# Predictions on the test set
y_pred_season = model_season.predict(X_test_season)
y_pred_type = model_type.predict(X_test_type)
y_pred = classifier.predict(X_test_scaled)

# Calculate accuracy
accuracy_season = accuracy_score(y_test_season, y_pred_season)
accuracy_type = accuracy_score(y_test_type, y_pred_type)
accuracy = accuracy_score(y_test, y_pred)

print(f'Accuracy for predicting Season: {accuracy_season}')
print(f'Accuracy for predicting Type: {accuracy_type}')
print(f'Accuracy for predicting Genre: {accuracy}')