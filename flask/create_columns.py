import pickle
import os

# Define paths
base_dir = os.path.dirname(os.path.abspath(__file__))
cols_path = os.path.join(base_dir, 'model_columns.pkl')

# Hardcoded feature list based on training logic
# 'step', 'amount', 'oldbalanceOrg', 'newbalanceOrig', 'oldbalanceDest', 'newbalanceDest'
# Plus dummy variables for 'type' (drop_first=True usually drops the first alphabetical one, typically 'CASH_IN' or similar, 
# but models can be tricky. Use the list from the error message as guide if needed).
# The error message said missing: type_CASH_OUT, type_DEBIT, type_PAYMENT, type_TRANSFER.
# This implies 'CASH_IN' was likely the dropped one (or reference).
# So we include these 4 explicit types.

model_columns = [
    'step',
    'amount',
    'oldbalanceOrg',
    'newbalanceOrig',
    'oldbalanceDest',
    'newbalanceDest',
    'type_CASH_OUT',
    'type_DEBIT',
    'type_PAYMENT',
    'type_TRANSFER'
]

print(f"Saving hardcoded model columns: {model_columns}")

# Save
pickle.dump(model_columns, open(cols_path, 'wb'))
print(f"Saved model columns to {cols_path}")
