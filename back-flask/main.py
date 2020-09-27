import os

from flask import Flask

from api.user import user

app = Flask(__name__)
app.register_blueprint(user)


@app.route('/')
def hello_world():
    return 'Hello, World!'


if __name__ == '__main__':
    # for deployment
    # to make it work for both production and development
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
# Run with export FLASK_APP=main.py; python -m flask run
