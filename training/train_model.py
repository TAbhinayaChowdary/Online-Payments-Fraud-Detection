import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import os

# Set paths
base_dir = os.path.dirname(os.path.abspath(__file__))
# Correct path to data based on user structure
data_path = os.path.join(base_dir, '..', 'data', 'PS_20174392719_1491204439457_log.csv')
model_path_training_pkl = os.path.join(base_dir, 'payments.pkl')
model_path_flask_pkl = os.path.join(base_dir, '..', 'flask', 'payments.pkl')
cols_path_flask = os.path.join(base_dir, '..', 'flask', 'model_columns.pkl')

print("Starting training process...")

if not os.path.exists(data_path):
    print(f"Error: Dataset not found at {data_path}")
    exit(1)

print("Loading dataset...")
# Read limited rows for faster demonstration (e.g., 100k rows) as full dataset is huge
# Remove 'nrows=100000' to use full dataset if desired.
df = pd.read_csv(data_path, nrows=100000) 

print("Preprocessing data...")
# Drop unnecessary columns
df = df.drop(['nameOrig', 'nameDest', 'isFlaggedFraud'], axis=1)

# Handle categorical values
# This will create columns like type_CASH_OUT, type_DEBIT, etc.
df = pd.get_dummies(df, columns=['type'], drop_first=True)

# Split data
X = df.drop('isFraud', axis=1)
y = df['isFraud']

# Save the column names so the app can recreate the structure
model_columns = list(X.columns)
pickle.dump(model_columns, open(cols_path_flask, 'wb'))
print(f"Model columns saved to {cols_path_flask}: {model_columns}")

print("Splitting into train and test sets...")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("Training Random Forest model...")
model = RandomForestClassifier(n_estimators=10, random_state=42) 
model.fit(X_train, y_train)

print("Evaluating model...")
y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {acc:.4f}")

print("Saving model...")
pickle.dump(model, open(model_path_training_pkl, 'wb'))
pickle.dump(model, open(model_path_flask_pkl, 'wb'))

print(f"Model saved to {model_path_training_pkl} and {model_path_flask_pkl}")
print("Done.")
