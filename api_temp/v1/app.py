#!/usr/bin/python3
"""Flask Application Server"""
from flask import Flask, make_response
from models import storage
from api.v1.views import app_views
from api.v1.functions import prettify
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def disconnect(message):
    """Close connection to storage engine"""
    storage.close()


@app.errorhandler(404)
def error404(err):
    """Custom error message"""
    resp = make_response(prettify({'error': 'Not found'}))
    resp.headers['Content-Type'] = 'application/json'
    return resp, 404


if __name__ == "__main__":
    app.run(host=getenv('HBNB_API_HOST', '0.0.0.0'),
            port=getenv('HBNB_API_PORT', 5000),
            threaded=True)
