from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

# Run with export FLASK_APP=main.py; python -m flask run
