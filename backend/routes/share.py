import datetime
import uuid

from flask import Blueprint, jsonify, request

from auth_utils import require_auth
from db import lists_collection, shares_collection, tasks_collection
from routes import serialize_doc, to_object_id

share_bp = Blueprint("share", __name__)


@share_bp.post("/lists/<list_id>")
@require_auth
def create_share_link(list_id):
    object_id = to_object_id(list_id)
    if not object_id:
        return jsonify({"message": "List not found"}), 404

    todo_list = lists_collection.find_one({"_id": object_id, "user_id": request.user_id})
    if not todo_list:
        return jsonify({"message": "List not found"}), 404

    share = shares_collection.find_one({"list_id": list_id, "user_id": request.user_id})
    if not share:
        share = {
            "share_id": uuid.uuid4().hex,
            "list_id": list_id,
            "user_id": request.user_id,
            "created_at": datetime.datetime.utcnow().isoformat(),
        }
        shares_collection.insert_one(share)

    frontend_url = request.headers.get("Origin") or "http://localhost:5173"
    return jsonify(
        {
            "message": "Share link ready",
            "share_id": share["share_id"],
            "share_url": f"{frontend_url}/share/{share['share_id']}",
        }
    ), 200


@share_bp.get("/<share_id>")
def get_shared_list(share_id):
    share = shares_collection.find_one({"share_id": share_id})
    if not share:
        return jsonify({"message": "Shared list not found"}), 404

    list_object_id = to_object_id(share["list_id"])
    todo_list = lists_collection.find_one({"_id": list_object_id})
    if not todo_list:
        return jsonify({"message": "Shared list not found"}), 404

    tasks = [
        serialize_doc(task)
        for task in tasks_collection.find({"list_id": share["list_id"], "user_id": share["user_id"]}).sort("created_at", -1)
    ]
    return jsonify({"list": serialize_doc(todo_list), "tasks": tasks}), 200
