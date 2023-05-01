#!/usr/bin/python3
""" helper functions """
import json


def prettify(dict_obj):
    """prettily serializes dictionary objects to json string"""
    return json.dumps(dict_obj, indent=2) + "\n"
