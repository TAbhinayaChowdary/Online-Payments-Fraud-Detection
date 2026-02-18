# Online Payments Fraud Detection

This project predicts whether an online payment transaction is fraudulent or not using Machine Learning (Random Forest Classification). It provides a web interface built with Flask for users to input transaction details and receive real-time predictions.

## Project Structure
- `flask/`: Contains the Flask web application code (`app.py`), templates, and static files.
- `training/`: Contains the Jupyter Notebook (`ONLINE PAYMENTS FRAUD DETECTION.ipynb`) and python scripts for data analysis, preprocessing, and model training.
- `data/`: (Not included in repo) Should contain the dataset `PS_20174392719_1491204439457_log.csv`.
- `flask/payments.pkl`: The trained Random Forest model (serialized).
- `flask/model_columns.pkl`: List of feature columns expected by the model.

## Setup & Usage

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/TAbhinayaChowdary/Online-Payments-Fraud-Detection.git
    cd Online-Payments-Fraud-Detection
    ```

2.  **Install Dependencies:**
    ```bash
    pip install flask pandas numpy scikit-learn matplotlib seaborn
    ```

3.  **Run the Web Application:**
    Navigate to the project root and run:
    ```bash
    python flask/app.py
    ```
    Access the app at `http://127.0.0.1:5000`.

4.  **Train the Model (Optional):**
    If you want to retrain the model with new data:
    ```bash
    python training/train_model.py
    # or open the Jupyter Notebook
    ```

## Dataset
The dataset used is the "Online Payments Fraud Detection Dataset" (e.g., from Kaggle). It contains features like:
- `step`: Unit of time (1 step = 1 hour)
- `type`: Transaction type (CASH-IN, CASH-OUT, DEBIT, PAYMENT, TRANSFER)
- `amount`: Amount of the transaction
- `oldbalanceOrg`: Initial balance of origin account
- `newbalanceOrig`: New balance of origin account
- `oldbalanceDest`: Initial balance of destination account
- `newbalanceDest`: New balance of destination account
- `isFraud`: Target variable (0 or 1)

## Screenshots
### Home Page
<img width="1897" height="867" alt="image" src="https://github.com/user-attachments/assets/704080c0-994f-49d5-95f8-7bf2025b6911" />

### Prediction Page
<img width="1919" height="866" alt="image" src="https://github.com/user-attachments/assets/1b6f269d-d08f-4862-b2c8-fd0ad4089d4e" />

### Result Page
<img width="1918" height="867" alt="image" src="https://github.com/user-attachments/assets/4664b078-cdce-4568-b316-806a4274199b" />



