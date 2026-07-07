import os
import jwt
import datetime
from functools import wraps
from pathlib import Path

from flask import request, jsonify
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent / ".env")

def _read_env(name, default):
    value = os.getenv(name, "").strip()
    if not value or value.lower().startswith("any_random_") or value.lower().endswith("_here"):
        return default
    return value


SECRET = _read_env("JWT_SECRET", "dev-jwt-secret-change-me")


def create_token(user_id):
    payload = {
        "user_id": str(user_id),
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=7),
    }
    token = jwt.encode(payload, SECRET, algorithm="HS256")
    return token


def require_auth(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return jsonify({"message": "No token, access denied"}), 401

        try:
            parts = auth_header.split()
            if len(parts) != 2 or parts[0].lower() != "bearer":
                return jsonify({"message": "Invalid authorization header"}), 401

            token = parts[1]
            decoded = jwt.decode(token, SECRET, algorithms=["HS256"])
            user_id = decoded.get("user_id")
            if not user_id:
                return jsonify({"message": "Invalid or expired token"}), 401
            request.user_id = user_id
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token has expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "Invalid or expired token"}), 401

        return f(*args, **kwargs)

    return wrapper
