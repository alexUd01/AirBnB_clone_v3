#!/usr/bin/python3
"""Create route"""
from api.v1.views import app_views
from flask import make_response
from models import storage
from api.v1.functions import prettify


@app_views.route('/status', strict_slashes=False)
def status():
    """Return api status"""
    resp = make_response(prettify({'status': 'OK'}))
    resp.headers['Content-Type'] = 'application/json'
    return resp


@app_views.route('/stats', strict_slashes=False)
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
