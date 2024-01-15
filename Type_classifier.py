# -*- coding: utf-8 -*-
"""
Created on Sat Jan 13 13:54:29 2024

@author: madha
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import SMOTE

# Loading the data
df = pd.read_csv('cleaned_dataset2023_unknown.csv')

value_to_drop = 'UNKNOWN'
df = df[df['Type'] != value_to_drop]

# Target column
X = df[['Rank', 'Popularity', 'Favorites', 'Weighted_Score', 'Members']]
y = df['Type']

# Use LabelEncoder to convert string labels to numeric format
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

# Handle class imbalance using SMOTE
smote = SMOTE(random_state=42)
X_resampled, y_resampled = smote.fit_resample(X, y_encoded)

# Divide dataset
X_train, X_test, y_train, y_test = train_test_split(X_resampled, y_resampled, test_size=0.2, random_state=42)

# Fixed hyperparameters
params = {
    'learning_rate': 0.2,
    'n_estimators': 400,
    'max_depth': 6,
    'min_child_weight': 3,
    'subsample': 0.9,
    'colsample_bytree': 0.9,
    'gamma': 0.1,
    'reg_alpha': 0.3,
    'reg_lambda': 0.3,
}

# Build XGBoost model
xgb_model = XGBClassifier(**params, random_state=42)
xgb_model.fit(X_train, y_train)

# Prediction
predictions = xgb_model.predict(X_test)

# Decode the predictions back to original labels
predicted_labels = label_encoder.inverse_transform(predictions)

# Display the predicted labels
print(predicted_labels)

# Find the most occurring prediction
most_occuring_prediction = pd.Series(predicted_labels).mode()[0]
print(f"Most Popular Type: {most_occuring_prediction}")