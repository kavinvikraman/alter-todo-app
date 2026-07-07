import datetime

import bcrypt
from flask import Blueprint, jsonify, request
from pymongo.errors import DuplicateKeyError

from auth_utils import create_token, require_auth
from db import users_collection
from routes import serialize_doc, to_object_id

auth_bp = Blueprint("auth", __name__)


@auth_bp.post("/signup")
def signup():
    data = request.get_json(silent=True) or {}
    name = (data.get("name") or "").strip()
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    if not name or not email or not password:
        return jsonify({"message": "Name, email, and password are required"}), 400

    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    user = {
        "name": name,
        "email": email,
        "password": hashed_password,
        "created_at": datetime.datetime.utcnow().isoformat(),
    }

    try:
        result = users_collection.insert_one(user)
    except DuplicateKeyError:
        return jsonify({"message": "Email already exists"}), 409

    user["_id"] = result.inserted_id
    user.pop("password", None)
    token = create_token(result.inserted_id)
    return jsonify({"message": "Signup successful", "token": token, "user": serialize_doc(user)}), 201


@auth_bp.post("/login")
def login():
    data = request.get_json(silent=True) or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    if not email or not password:
        return jsonify({"message": "Email and password are required"}), 400

    user = users_collection.find_one({"email": email})
    if not user or not bcrypt.checkpw(password.encode("utf-8"), user["password"].encode("utf-8")):
        return jsonify({"message": "Invalid email or password"}), 401

    token = create_token(user["_id"])
    user.pop("password", None)
    return jsonify({"message": "Login successful", "token": token, "user": serialize_doc(user)}), 200


@auth_bp.get("/me")
@require_auth
def me():
    user_id = to_object_id(request.user_id)
    user = users_collection.find_one({"_id": user_id}) if user_id else None
    if not user:
        return jsonify({"message": "User not found"}), 404

    user.pop("password", None)
    return jsonify({"user": serialize_doc(user)}), 200
