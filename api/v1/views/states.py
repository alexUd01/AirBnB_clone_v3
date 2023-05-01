#!/usr/bin/python3
"""A view for State objects that handles all default RESTFul API actions
"""
from api.v1.views import app_views
from models import storage
from models.state import State
from flask import make_response, request, abort
from api.v1.functions import prettify

allowed_methods_1 = ['GET', 'HEAD', 'OPTIONS', 'POST']
allowed_methods_2 = ['GET', 'HEAD', 'OPTIONS', 'PUT', 'DELETE']


@app_views.route('/states', methods=allowed_methods_1, strict_slashes=False)
@app_views.route('/states/<state_id>', methods=allowed_methods_2,
                 strict_slashes=False)
def states(state_id=None):
    """handles all default RESTFul API actions for `State` objects"""
    storage.reload()

    if request.method == 'GET':
        if state_id is None:  # handle GET request on route('/states')
            # Retrieve items from database
            all = []
            for item in storage.all(State).values():
                all.append(item.to_dict())
            resp = make_response(prettify(all))
            resp.headers['Content-Type'] = 'application/json'
            return resp
        else:  # handle GET request on route('states/<state_id>')
            try:
                key = 'State.{}'.format(state_id)
                obj = storage.all(State)[key]
            except KeyError:
                abort(404)
            else:
                resp = make_response(prettify(obj.to_dict()))
                resp.headers['Content-Type'] = 'application/json'
                return resp
    elif request.method == 'DELETE':
        if state_id is not None:
            try:
                key = "State.{}".format(state_id)
                obj = storage.all(State)[key]
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
            state_name = data['name']
        except KeyError:
            return "Missing name", 400
        except Exception:
            return "Not a JSON", 400
        else:
            new_state = State(**data)
            storage.new(new_state)
            storage.save()
            resp = make_response(prettify(new_state.to_dict()))
            resp.headers['Content-Type'] = 'application/json'
            return resp, 201
    elif request.method == 'PUT':
        storage.reload()
        if state_id is not None:
            key = "State.{}".format(state_id)
            try:
                data = request.get_json()
                state_obj = storage.all(State)[key]
            except KeyError:
                abort(404)
            except Exception:
                return "Not a JSON", 400
            else:
                for k, v in data.items():
                    if k not in ('id', 'created_at', 'updated_at'):
                        setattr(state_obj, k, v)
                storage.all(State)[key] = state_obj
                storage.save()
                resp = make_response(prettify(state_obj.to_dict()))
                resp.headers['Content-Type'] = 'application/json'
                return resp
