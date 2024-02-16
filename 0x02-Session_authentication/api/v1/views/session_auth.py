#!/usr/bin/env python3
""" Session Auth views """

from api.v1.views import app_views
from flask import jsonify, request, abort, make_response
from models.user import User
from os import getenv

SESSION_NAME = getenv("SESSION_NAME", "_my_session_id")


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def session_login():
    """ Handles Session authentication login """
    email = request.form.get('email')
    password = request.form.get('password')

    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400

    user = User.search({"email": email})
    if not user:
        return jsonify({"error": "no user found for this email"}), 404

    if not user[0].is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    auth = __import__('api.v1.app', fromlist=['auth']).auth
    session_id = auth.create_session(user[0].id)

    response = jsonify(user[0].to_json())
    response.set_cookie(SESSION_NAME, session_id)

    return response, 200


@app_views.route('/auth_session/logout', methods=['DELETE'], strict_slashes=False)
def session_logout():
    """ Handles Session authentication logout """
    from api.v1.app import auth
    if not auth.destroy_session(request):
        abort(404)
    return jsonify({}), 200
