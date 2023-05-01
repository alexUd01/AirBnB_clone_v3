#!/usr/bin/python3
"""A view for City objects that handles all default RESTFul API actions
"""
from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State
from flask import make_response, request, abort
from api.v1.functions import prettify
from datetime import datetime

allowed_methods_1 = ['GET', 'HEAD', 'OPTIONS', 'POST']
allowed_methods_2 = ['GET', 'HEAD', 'OPTIONS', 'PUT', 'DELETE']


@app_views.route('/cities', methods=allowed_methods_1, strict_slashes=False)
@app_views.route('/cities/<city_id>', methods=allowed_methods_2,
                 strict_slashes=False)
def cities(city_id=None):
    """handles all default RESTFul API actions for `City` objects"""
    storage.reload()

    if request.method == 'GET':
        if city_id is None:  # handle GET request on route('/cities')
            # Retrieve items from database
            all = []
            for item in storage.all(City).values():
                all.append(item.to_dict())
            resp = make_response(prettify(all))
            resp.headers['Content-Type'] = 'application/json'
            return resp
        else:  # handle GET request on route('cities/<city_id>')
            try:
                key = 'City.{}'.format(city_id)
                obj = storage.all(City)[key]
            except KeyError:
                abort(404)
            else:
                resp = make_response(prettify(obj.to_dict()))
                resp.headers['Content-Type'] = 'application/json'
                return resp
    elif request.method == 'DELETE':
        if city_id is not None:
            try:
                key = "City.{}".format(city_id)
                obj = storage.all(City)[key]
            except KeyError:
                abort(404)
            else:
                storage.delete(obj)
                storage.save()
                resp = make_response(prettify({}))
                resp.headers['Content-Type'] = 'application/json'
                return resp
    elif request.method == 'POST':
        try:
            data = request.get_json()
            city_name = data['name']
        except KeyError:
            return "Missing name\n", 400
        except Exception:
            return "Not a JSON\n", 400
        else:
            # Disallow created_at, updated_at and id
            if data.get('created_at', None):
                del data['created_at']
            if data.get('updated_at', None):
                del data['updated_at']
            if data.get('id', None):
                del data['id']
            new_city = City(**data)
            storage.new(new_city)
            storage.save()
            resp = make_response(prettify(new_city.to_dict()))
            resp.headers['Content-Type'] = 'application/json'
            return resp, 201
    elif request.method == 'PUT':
        storage.reload()
        if city_id is not None:
            key = "City.{}".format(city_id)
            try:
                data = request.get_json()
                city_obj = storage.all(City)[key]
            except KeyError:
                abort(404)
            except Exception:
                return "Not a JSON\n", 400
            else:
                for k, v in data.items():
                    # Disallow created_at, updated_at and id
                    if k not in ('id', 'created_at', 'updated_at'):
                        setattr(city_obj, k, v)
                        setattr(city_obj, 'updated_at', datetime.utcnow())
                storage.all(City)[key] = city_obj
                storage.save()
                resp = make_response(prettify(city_obj.to_dict()))
                resp.headers['Content-Type'] = 'application/json'
                return resp
# ---------------------- THE REMAINING IS INCOMPLETE ---------------------


@app_views.route('/states/<state_id>/cities', methods=allowed_methods_1,
                 strict_slashes=False)
@app_views.route('/states/<state_id>/cities/<city_id>',
                 methods=allowed_methods_2, strict_slashes=False)
def state_cities(state_id, city_id=None):
    """Handles `cities` located inside `State` objects"""
    # Ensure that `state_id` is valid
    try:
        state_key = "State.{}".format(state_id)
        storage.all(State)[state_key]
    except KeyError:
        abort(404)

    if request.method == 'GET':
        if city_id is None:  # route('/states/<state_id>/cities')
            all_cities = storage.all(City).values()
            same_state_cities = [a_city.to_dict() for a_city in all_cities
                                 if a_city.state_id == state_id]
            resp = make_response(prettify(same_state_cities))
            resp.headers['Content-Type'] = 'application/json'
            return resp
        else:  # route('/states/<state_id>/cities/<city_id>')
            try:
                city_key = "City.{}".format(city_id)
                a_city = storage.all(City)[city_key]
            except KeyError:
                abort(404)
            else:
                # Handle differently typed objects with same `id`
                if a_city.state_id != state_id:
                    abort(404)
                resp = make_response(prettify(a_city.to_dict()))
                resp.headers['Content-Type'] = 'application/json'
                return resp

    if request.method == 'DELETE':  # Not included in `Requirements` section
        pass  # Do Nothing

    
