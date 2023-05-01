#!/usr/bin/python3
"""Create route"""
from api.v1.views import app_views
import json
from flask import make_response
from models import storage


def prettify(dict_obj):
    """prettily serializes dictionary objects to json string"""
    if not isinstance(dict_obj, dict):
        raise TypeError('"dict_object" must be a python dictionary')
    return json.dumps(dict_obj, indent=2) + "\n"


@app_views.route('/status')
def status():
    """Return api status"""
    resp = make_response(prettify({'status': 'OK'}))
    resp.headers['Content-Type'] = 'application/json'
    return resp


@app_views.route('/stats')
def stats():
    """Return api stat"""
    stat = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    }
    resp = make_response(prettify(stat))
    resp.headers['Content-Type'] = 'application/json'
    return resp
