# -*- coding: utf-8 -*-
"""
Created on Wed Dec 13 10:53:11 2023

@author: yuyue
"""

import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder

file_path = r'archive\cleaned_dataset2023.csv'

df = pd.read_csv(file_path)

X = df[['Score', 'Rank', 'Popularity', 'Favorites', 'Scored By', 'Members']]
y = df['Type']

# Encoding the target variable 'Type' as it is categorical
le = LabelEncoder()
y_encoded = le.fit_transform(y)

# Splitting the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

# Creating the Decision Tree classifier
dt_classifier = DecisionTreeClassifier(random_state=42)

# Fitting the classifier to the training data
dt_classifier.fit(X_train, y_train)

# Predicting on the test data
y_pred = dt_classifier.predict(X_test)

# Calculating the accuracy of the classifier
accuracy = accuracy_score(y_test, y_pred)

print(f'Accuracy: {accuracy}')