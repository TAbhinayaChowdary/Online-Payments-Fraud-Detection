print("Starting debug application...")
try:
    from flask import Flask
    print("Imported Flask successfully.")
except ImportError:
    print("Failed to import Flask!")
    exit(1)

app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>Debug App is Working!</h1><p>If you see this, Flask is fine.</p>"

if __name__ == "__main__":
    print("Starting server on port 5000...")
    app.run(host='0.0.0.0', port=5000, debug=True)
