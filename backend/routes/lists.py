import datetime

from flask import Blueprint, jsonify, request

from auth_utils import require_auth
from db import lists_collection, tasks_collection
from routes import serialize_doc, to_object_id

lists_bp = Blueprint("lists", __name__)


def find_user_list(list_id):
    object_id = to_object_id(list_id)
    if not object_id:
        return None
    return lists_collection.find_one({"_id": object_id, "user_id": request.user_id})


@lists_bp.get("/")
@require_auth
def get_lists():
    lists = []
    for todo_list in lists_collection.find({"user_id": request.user_id}).sort("created_at", -1):
        item = serialize_doc(todo_list)
        item["task_count"] = tasks_collection.count_documents({"list_id": item["id"], "user_id": request.user_id})
        lists.append(item)
    return jsonify({"lists": lists}), 200


@lists_bp.post("/")
@require_auth
def create_list():
    data = request.get_json(silent=True) or {}
    name = (data.get("name") or "").strip()
    if not name:
        return jsonify({"message": "List name is required"}), 400

    todo_list = {
        "name": name,
        "user_id": request.user_id,
        "created_at": datetime.datetime.utcnow().isoformat(),
        "updated_at": datetime.datetime.utcnow().isoformat(),
    }
    result = lists_collection.insert_one(todo_list)
    todo_list["_id"] = result.inserted_id
    return jsonify({"message": "List created", "list": serialize_doc(todo_list)}), 201


@lists_bp.get("/<list_id>")
@require_auth
def get_list(list_id):
    todo_list = find_user_list(list_id)
    if not todo_list:
        return jsonify({"message": "List not found"}), 404
    return jsonify({"list": serialize_doc(todo_list)}), 200


@lists_bp.patch("/<list_id>")
@require_auth
def update_list(list_id):
    todo_list = find_user_list(list_id)
    if not todo_list:
        return jsonify({"message": "List not found"}), 404

    data = request.get_json(silent=True) or {}
    name = (data.get("name") or "").strip()
    if not name:
        return jsonify({"message": "List name is required"}), 400

    lists_collection.update_one(
        {"_id": todo_list["_id"]},
        {"$set": {"name": name, "updated_at": datetime.datetime.utcnow().isoformat()}},
    )
    todo_list["name"] = name
    return jsonify({"message": "List updated", "list": serialize_doc(todo_list)}), 200


@lists_bp.delete("/<list_id>")
@require_auth
def delete_list(list_id):
    todo_list = find_user_list(list_id)
    if not todo_list:
        return jsonify({"message": "List not found"}), 404

    lists_collection.delete_one({"_id": todo_list["_id"]})
    tasks_collection.delete_many({"list_id": str(todo_list["_id"]), "user_id": request.user_id})
    return jsonify({"message": "List deleted"}), 200


@lists_bp.get("/<list_id>/stats")
@require_auth
def list_stats(list_id):
    todo_list = find_user_list(list_id)
    if not todo_list:
        return jsonify({"message": "List not found"}), 404

    query = {"list_id": str(todo_list["_id"]), "user_id": request.user_id}
    tasks = list(tasks_collection.find(query))
    total = len(tasks)
    completed = len([task for task in tasks if task.get("completed")])
    tag_counts = {}
    no_tag = 0

    for task in tasks:
        tags = task.get("tags", [])
        if not tags:
            no_tag += 1
        for tag in tags:
            tag_counts[tag] = tag_counts.get(tag, 0) + 1

    return jsonify(
        {
            "stats": {
                "total": total,
                "completed": completed,
                "pending": total - completed,
                "tags": tag_counts,
                "no_tag": no_tag,
            }
        }
    ), 200
