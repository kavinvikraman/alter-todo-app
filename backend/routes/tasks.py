import datetime

from flask import Blueprint, jsonify, request

from auth_utils import require_auth
from db import lists_collection, tasks_collection
from routes import serialize_doc, to_object_id

tasks_bp = Blueprint("tasks", __name__)


def find_user_task(task_id):
    object_id = to_object_id(task_id)
    if not object_id:
        return None
    return tasks_collection.find_one({"_id": object_id, "user_id": request.user_id})


def user_owns_list(list_id):
    object_id = to_object_id(list_id)
    if not object_id:
        return False
    return lists_collection.find_one({"_id": object_id, "user_id": request.user_id}) is not None


@tasks_bp.get("/")
@require_auth
def get_tasks():
    list_id = request.args.get("list_id")
    query = {"user_id": request.user_id}
    if list_id:
        if not user_owns_list(list_id):
            return jsonify({"message": "List not found"}), 404
        query["list_id"] = list_id

    tasks = [serialize_doc(task) for task in tasks_collection.find(query).sort("created_at", -1)]
    return jsonify({"tasks": tasks}), 200


@tasks_bp.get("/tags")
@require_auth
def get_tags():
    list_id = request.args.get("list_id")
    query = {"user_id": request.user_id}
    if list_id:
        if not user_owns_list(list_id):
            return jsonify({"message": "List not found"}), 404
        query["list_id"] = list_id

    tag_counts = {}
    for task in tasks_collection.find(query, {"tags": 1}):
        for tag in task.get("tags", []):
            tag_counts[tag] = tag_counts.get(tag, 0) + 1
    return jsonify({"tags": tag_counts}), 200


@tasks_bp.post("/")
@require_auth
def create_task():
    data = request.get_json(silent=True) or {}
    list_id = data.get("list_id")
    title = (data.get("title") or "").strip()
    tags = data.get("tags") or []

    if not list_id or not title:
        return jsonify({"message": "list_id and title are required"}), 400
    if not user_owns_list(list_id):
        return jsonify({"message": "List not found"}), 404
    if not isinstance(tags, list):
        return jsonify({"message": "Tags must be an array"}), 400

    now = datetime.datetime.utcnow().isoformat()
    task = {
        "list_id": list_id,
        "user_id": request.user_id,
        "title": title,
        "description": data.get("description", ""),
        "completed": bool(data.get("completed", False)),
        "tags": [str(tag).strip() for tag in tags if str(tag).strip()],
        "created_at": now,
        "updated_at": now,
    }
    result = tasks_collection.insert_one(task)
    task["_id"] = result.inserted_id
    return jsonify({"message": "Task created", "task": serialize_doc(task)}), 201


@tasks_bp.get("/<task_id>")
@require_auth
def get_task(task_id):
    task = find_user_task(task_id)
    if not task:
        return jsonify({"message": "Task not found"}), 404
    return jsonify({"task": serialize_doc(task)}), 200


@tasks_bp.patch("/<task_id>")
@require_auth
def update_task(task_id):
    task = find_user_task(task_id)
    if not task:
        return jsonify({"message": "Task not found"}), 404

    data = request.get_json(silent=True) or {}
    updates = {"updated_at": datetime.datetime.utcnow().isoformat()}

    if "title" in data:
        title = (data.get("title") or "").strip()
        if not title:
            return jsonify({"message": "Task title cannot be empty"}), 400
        updates["title"] = title
    if "description" in data:
        updates["description"] = data.get("description", "")
    if "completed" in data:
        updates["completed"] = bool(data.get("completed"))
    if "tags" in data:
        if not isinstance(data["tags"], list):
            return jsonify({"message": "Tags must be an array"}), 400
        updates["tags"] = [str(tag).strip() for tag in data["tags"] if str(tag).strip()]

    tasks_collection.update_one({"_id": task["_id"]}, {"$set": updates})
    task.update(updates)
    return jsonify({"message": "Task updated", "task": serialize_doc(task)}), 200


@tasks_bp.delete("/<task_id>")
@require_auth
def delete_task(task_id):
    task = find_user_task(task_id)
    if not task:
        return jsonify({"message": "Task not found"}), 404

    tasks_collection.delete_one({"_id": task["_id"]})
    return jsonify({"message": "Task deleted"}), 200


@tasks_bp.post("/<task_id>/tags")
@require_auth
def add_tag(task_id):
    task = find_user_task(task_id)
    if not task:
        return jsonify({"message": "Task not found"}), 404

    data = request.get_json(silent=True) or {}
    tag = str(data.get("tag") or "").strip()
    if not tag:
        return jsonify({"message": "Tag is required"}), 400

    tasks_collection.update_one({"_id": task["_id"]}, {"$addToSet": {"tags": tag}})
    task["tags"] = sorted(set(task.get("tags", []) + [tag]))
    return jsonify({"message": "Tag added", "task": serialize_doc(task)}), 200


@tasks_bp.delete("/<task_id>/tags/<tag>")
@require_auth
def remove_tag(task_id, tag):
    task = find_user_task(task_id)
    if not task:
        return jsonify({"message": "Task not found"}), 404

    tasks_collection.update_one({"_id": task["_id"]}, {"$pull": {"tags": tag}})
    task["tags"] = [item for item in task.get("tags", []) if item != tag]
    return jsonify({"message": "Tag removed", "task": serialize_doc(task)}), 200
