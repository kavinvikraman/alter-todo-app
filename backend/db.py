import os
from pathlib import Path

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv(Path(__file__).resolve().parent / ".env")


def _read_env(name, default):
    value = os.getenv(name, "").strip()
    if not value or value.lower().startswith("your_") or value.lower().endswith("_here"):
        return default
    return value


MONGO_URI = _read_env("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB_NAME = _read_env("MONGO_DB_NAME", "todo_app")

client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=2000, connectTimeoutMS=2000)
db = client[MONGO_DB_NAME]

users_collection = db["users"]
todo_lists_collection = db["todo_lists"]
tasks_collection = db["tasks"]
shares_collection = db["shares"]

# Backward-compatible alias for existing route imports.
lists_collection = todo_lists_collection


def ping_db():
    client.admin.command("ping")
    return True


def ensure_indexes():
    users_collection.create_index("email", unique=True)
    todo_lists_collection.create_index([("user_id", 1), ("created_at", -1)])
    tasks_collection.create_index([("user_id", 1), ("list_id", 1), ("created_at", -1)])
    shares_collection.create_index("share_id", unique=True)
