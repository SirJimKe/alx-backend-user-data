#!/usr/bin/env python3
"""app module"""
from flask import Flask, request, jsonify, abort, make_response
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route("/")
def welcome():
    """welcome message"""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def users():
    """registers new users"""
    email = request.form.get("email")
    password = request.form.get("password")

    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"}), 200
    except ValueError as e:
        return jsonify({"message": str(e)}), 400


@app.route("/sessions", methods=["POST"])
def login():
    "verify login"
    email = request.form.get("email")
    password = request.form.get("password")

    if email is None or password is None:
        abort(400)

    if not AUTH.valid_login(email, password):
        abort(401)

    session_id = AUTH.create_session(email)
    if session_id is None:
        abort(500)

    response = jsonify({"email": email, "message": "logged in"})
    response.set_cookie("session_id", session_id)
    return response


@app.route("/sessions", methods=["DELETE"])
def logout():
    """Logout user"""
    session_id = request.cookies.get("session_id")

    if session_id is None:
        return jsonify({"message": "Session ID not found"}), 403

    user = AUTH.get_user_from_session_id(session_id)

    if user is None:
        return jsonify({"message": "Invalid session ID"}), 403

    AUTH.destroy_session(user.id)

    return redirect("/")


@app.route("/profile", methods=["GET"])
def profile():
    """Get user profile"""
    session_id = request.cookies.get("session_id")

    if session_id is None:
        return jsonify({"message": "Session ID not found"}), 403

    user = AUTH.get_user_from_session_id(session_id)

    if user is None:
        return jsonify({"message": "Invalid session ID"}), 403

    return jsonify({"email": user.email}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
