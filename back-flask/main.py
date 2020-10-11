import os

from flask import Flask
from flask_cors import CORS

from api.item import item
from api.request import request
from api.user import user
from spec import get_spec_as_html

app = Flask(__name__)
CORS(app)
app.config['CORS_ORIGINS'] = 'http://localhost:3000'

app.register_blueprint(user)
app.register_blueprint(item)
app.register_blueprint(request)

@app.route('/')
def get_api_spec():
    return get_spec_as_html()

if __name__ == '__main__':
    # for deployment
    # to make it work for both production and development
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
# Run with export FLASK_APP=main.py; python -m flask run
