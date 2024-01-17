# -*- coding: utf-8 -*-
"""
Created on Sat Jan 13 15:10:48 2024

@author: yuyue
"""

import pandas as pd
from sklearn.preprocessing import MultiLabelBinarizer

# Assuming 'df' is your DataFrame
#loading the data
df = pd.read_csv(r"C:\Semester3YYYY\DataLiteracy\archive\cleaned_dataset2023.csv")

# The features you will use to predict genres
X = df[['Rank', 'Popularity', 'Favorites', 'Weighted_Score', 'Members']]

# Preprocessing the 'Genres' column
# Assuming the 'Genres' column contains strings of genres separated by commas
genres_list = df['Genres'].apply(lambda x: x.split(', '))

# Initialize the MultiLabelBinarizer
mlb = MultiLabelBinarizer()

# Fit and transform the genres_list to a binary matrix
y = mlb.fit_transform(genres_list)

# Now, 'y' is a binary matrix with a column for each genre indicating the presence or absence of the genre

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.multiclass import OneVsRestClassifier

# Split the dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize the OneVsRestClassifier with a LogisticRegression classifier
model = OneVsRestClassifier(LogisticRegression())

# Train the model
model.fit(X_train, y_train)

# Make predictions
predictions = model.predict(X_test)

predicted_genres = mlb.inverse_transform(predictions)