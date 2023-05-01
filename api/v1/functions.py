#!/usr/bin/python3
""" helper functions """
import json


def prettify(dict_obj):
    """prettily serializes dictionary objects to json string"""
    if not isinstance(dict_obj, dict):
        raise TypeError('"dict_object" must be a python dictionary')
    return json.dumps(dict_obj, indent=2) + "\n"
