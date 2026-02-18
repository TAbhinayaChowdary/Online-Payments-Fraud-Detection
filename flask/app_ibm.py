from flask import Flask, render_template, request
import pickle
import numpy as np

app = Flask(__name__)

# Placeholder for IBM model loading if needed or specific IBM logic
# model = ... 

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Placeholder for prediction logic using IBM services
    output = "Legitimate" # Dummy output
    return render_template('submit.html', prediction_text='Transaction is likelihood to be {}'.format(output))

if __name__ == "__main__":
    app.run(debug=True)
