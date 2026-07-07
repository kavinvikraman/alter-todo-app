from bson import ObjectId
from bson.errors import InvalidId


def to_object_id(value):
    try:
        return ObjectId(value)
    except (InvalidId, TypeError):
        return None


def serialize_doc(doc):
    if not doc:
        return None

    result = {}
    for key, value in doc.items():
        if key == "_id":
            result["id"] = str(value)
        elif isinstance(value, ObjectId):
            result[key] = str(value)
        else:
            result[key] = value
    return result
