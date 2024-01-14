# -*- coding: utf-8 -*-
"""
Created on Wed Dec 13 10:53:11 2023

@author: yuyue
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import classification_report
from sklearn.preprocessing import StandardScaler

#loading the data
df = pd.read_csv('archive/cleaned_dataset2023.csv')

#target column
X = df[['Rank', 'Popularity', 'Favorites', 'Weighted_Score', 'Members']]
y = df['Type']

# Standardize features by removing the mean and scaling to unit variance
# SVMs assume that the data it works with is in a standard range
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

#divide dataset
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

#build SVM model
# Using the radial basis function (RBF) kernel
model = SVC(kernel='rbf', gamma='scale', C=100)

#train the model
model.fit(X_train, y_train)

#prediction
predictions = model.predict(X_test)

#evaluation
result = classification_report(y_test, predictions, zero_division=0)

print(result)

