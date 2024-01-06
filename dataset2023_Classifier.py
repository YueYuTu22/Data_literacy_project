# -*- coding: utf-8 -*-
"""
Created on Wed Dec 13 10:53:11 2023

@author: yuyue
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

#loading the data
df = pd.read_csv('archive/cleaned_dataset2023.csv')

type_counts = df['Type'].value_counts()
Special_count = type_counts.get('Special', 0)
TV_count = type_counts.get('TV', 0)
Movie_count = type_counts.get('Movie', 0)
ONA_count = type_counts.get('ONA', 0)
ONA_count = type_counts.get('OVA', 0)

#target column
X = df[['Rank', 'Popularity', 'Favorites', 'Weighted_Score', 'Members']] 
y = df['Type']

#divide dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#build logistic regression model
model = LogisticRegression(
    multi_class='multinomial', 
    solver='newton-cg', 
    C=0.01,  #Regularization
    max_iter=500,  #Max iteration
    tol=0.0001   #Tolerance
)

#train the model
model.fit(X_train, y_train)

#prediction
predictions = model.predict(X_test)
#waring! The line search algorithm did not converge

result = classification_report(y_test, predictions)

