from flask import Flask, render_template, request, jsonify
print("Custom Debug: Importing libraries...")
import pickle
import pandas as pd
import numpy as np
import os

app = Flask(__name__)

# Load model and columns
base_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(base_dir, 'payments.pkl')
cols_path = os.path.join(base_dir, 'model_columns.pkl')

model = None
model_cols = None

try:
    if os.path.exists(model_path):
        # Custom Debug: Try loading with a different approach or just print
        print(f"Loading model from {model_path}...")
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        print("Loaded model successfully!")
    else:
        print(f"Warning: Model file not found at {model_path}. Run training/train_model.py first.")
except Exception as e:
    print(f"Error loading model: {e}")

try:
    if os.path.exists(cols_path):
        model_cols = pickle.load(open(cols_path, 'rb'))
    else:
        print(f"Warning: Model columns file not found at {cols_path}")
except Exception as e:
    print(f"Error loading columns: {e}")

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'GET':
         return render_template('predict.html')
         
    try:
        # Get input features from form
        # We need to make sure we parse these correctly
        # The form inputs: step, type, amount, oldbalanceOrg, newbalanceOrig, oldbalanceDest, newbalanceDest
        step = int(request.form['step'])
        type_val = request.form['type'].upper() # Ensure uppercase to match dataset
        amount = float(request.form['amount'])
        # nameOrig = request.form['nameOrig'] # Ignored
        oldbalanceOrg = float(request.form['oldbalanceOrg'])
        newbalanceOrig = float(request.form['newbalanceOrig'])
        # nameDest = request.form['nameDest'] # Ignored
        oldbalanceDest = float(request.form['oldbalanceDest'])
        newbalanceDest = float(request.form['newbalanceDest'])

        # Create DataFrame for prediction
        # The column names must match what was used during training BEFORE get_dummies
        # Training used: step, type, amount, oldbalanceOrg, newbalanceOrig, oldbalanceDest, newbalanceDest
        input_data = pd.DataFrame([[step, type_val, amount, oldbalanceOrg, newbalanceOrig, oldbalanceDest, newbalanceDest]],
                                  columns=['step', 'type', 'amount', 'oldbalanceOrg', 'newbalanceOrig', 'oldbalanceDest', 'newbalanceDest'])
        
        # Preprocess
        # One-Hot Encode 'type'
        input_data = pd.get_dummies(input_data, columns=['type'], drop_first=True)
        
        # Align with model columns
        if model_cols:
            # Get missing columns
            # We need to ensure input_data has all columns model expects (from model_cols)
            # And ONLY those columns, in the CORRECT ORDER
            
            # 1. Add missing columns with 0
            for col in model_cols:
                if col not in input_data.columns:
                    input_data[col] = 0
            
            # 2. Select only the relevant columns in correct order
            input_data = input_data[model_cols]

        # Predict
        if model:
            # prediction is an array, e.g. [0] or [1]
            prediction = model.predict(input_data)
            output = "['is Fraud']" if prediction[0] == 1 else "['is not Fraud']"
        else:
            output = "['Model not loaded']"

        return render_template('submit.html', prediction_text='{}'.format(output))
    except Exception as e:
        # Print error to terminal for debugging
        print(f"Prediction Error: {e}")
        return render_template('submit.html', prediction_text='Error: {}'.format(str(e)))

@app.route('/predict_api', methods=['POST'])
def predict_api():
    '''
    For direct API calls
    '''
    return jsonify({"error": "Not implemented yet"})

if __name__ == "__main__":
    print("Starting Flask server on http://127.0.0.1:5000")
    # Run slightly differently to avoid potential conflicts
    app.run(host='0.0.0.0', port=5000, debug=True)
