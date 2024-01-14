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


