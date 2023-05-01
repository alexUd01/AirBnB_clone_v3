#!/usr/bin/python3
"""Create route"""
from api.v1.views import app_views
import json
from flask import make_response


@app_views.route('/status')
def status():
    """Return api status"""
    resp = make_response(json.dumps({'status': 'OK'}, indent=2) + '\n')
    resp.headers['Content-Type'] = 'application/json'
    return resp


@app_views.route('/stats')
def stats():
    """Return api stat"""
    
