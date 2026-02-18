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
        step = int(request.form['step'])
        type_val = request.form['type'].upper()
        amount = float(request.form['amount'])
        # nameOrig ignored
        oldbalanceOrg = float(request.form['oldbalanceOrg'])
        newbalanceOrig = float(request.form['newbalanceOrig'])
        # nameDest ignored
        oldbalanceDest = float(request.form['oldbalanceDest'])
        newbalanceDest = float(request.form['newbalanceDest'])

        # Manual Label Encoding to match model training (Alphabetical: CASH_IN=0, CASH_OUT=1, DEBIT=2, PAYMENT=3, TRANSFER=4)
        type_mapping = {
            'CASH_IN': 0, 
            'CASH_OUT': 1, 
            'DEBIT': 2, 
            'PAYMENT': 3, 
            'TRANSFER': 4
        }
        # Default to PAYMENT(3) or TRANSFER(4) if unknown? Or Raise error. 
        # For safety, let's look it up or default to 4 (TRANSFER is common for fraud).
        type_encoded = type_mapping.get(type_val, 4) 

        # Create DataFrame with exact columns expected by SVC model (Label Encoded)
        # Expected order: step, type, amount, oldbalanceOrg, newbalanceOrig, oldbalanceDest, newbalanceDest
        feature_names = ['step', 'type', 'amount', 'oldbalanceOrg', 'newbalanceOrig', 'oldbalanceDest', 'newbalanceDest']
        
        input_data = pd.DataFrame([[
            step, 
            type_encoded, 
            amount, 
            oldbalanceOrg, 
            newbalanceOrig, 
            oldbalanceDest, 
            newbalanceDest
        ]], columns=feature_names)
        
        # Verify model loading
        if model:
            print(f"Predicting with features: {feature_names}")
            print(f"Input values: {input_data.values}")
            
            prediction = model.predict(input_data)
            
            # Prediction is likely 0 or 1
            # Check shape/type
            pred_val = prediction[0]
            output = "['is Fraud']" if pred_val == 1 else "['is not Fraud']"
        else:
            output = "['Model not loaded - Check server logs']"

        return render_template('submit.html', prediction_text=str(output))
    except Exception as e:
        print(f"Prediction Error: {e}")
        return render_template('submit.html', prediction_text=f'Error: {str(e)}')

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
