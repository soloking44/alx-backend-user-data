#!/usr/bin/env python3
"""
Module app
Basic Flask app
"""
from flask import Flask, jsonify, request, abort, redirect, url_for
from auth import Auth


AUTH = Auth()
app = Flask(__name__)


@app.route("/", methods=['GET'], strict_slashes=False)
def home():
    """Home route
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def users():
    """Register user
    """
    email = request.form.get("email")
    password = request.form.get("password")
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": f"{email}", "message": "user created"}), 200
    except Exception:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login():
    """Authenticate the user using user credential
    """
    email = request.form.get("email")
    password = request.form.get("password")
    session_id = AUTH.create_session(email=email)
    if session_id is None:
        abort(401)
    valid_password = AUTH.valid_login(email, password)
    if not valid_password:
        abort(401)
    response = jsonify({"email": f"{email}", "message": "logged in"})
    response.set_cookie("session_id", session_id)
    return response


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout():
    """Delete session id
    """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect(url_for("home"))


@app.route("/profile", methods=["GET"], strict_slashes=False)
def profile():
    """Display user information
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        return jsonify({"email": user.email}), 200
    else:
        abort(403)


@app.route("/reset_password", methods=["POST"], strict_slashes=False)
def get_reset_password_token():
    """Generate token to reset password
    """
    email = request.form.get("email")
    session_id = AUTH.create_session(email)
    if not session_id:
        abort(403)
    token = AUTH.get_reset_password_token(email)
    return jsonify({"email": f"{email}", "reset_token": f"{token}"}), 200


@app.route("/reset_password", methods=["PUT"], strict_slashes=False)
def update_password():
    """update user's password
    """
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")
    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify({"email": f"{email}",
                       "message": "Password updated"}), 200
    except Exception:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
