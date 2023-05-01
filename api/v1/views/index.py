#!/usr/bin/python3
"""Create route"""
from api.v1.views import app_views
import json


@app_views.route('/status')
def status():
    """Return api status"""
    return json.dumps({'status': 'OK'}) + '\n'
