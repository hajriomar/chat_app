from bson import ObjectId
from chat_app.db.mongo import get_users_collection

def create_user(user_doc):
    return get_users_collection().insert_one(user_doc)

def get_user_by_username(username):
    return get_users_collection().find_one({"username": username})

def get_user_by_id(user_id):
    if isinstance(user_id, str):
        user_id = ObjectId(user_id)
    return get_users_collection().find_one({"_id": user_id})

def get_users_by_ids(user_ids):
    return list(get_users_collection().find({
        "_id": {"$in": user_ids}
    }))

def get_all_users_except(username):
    return list(get_users_collection().find({
        "username": {"$ne": username}
    }))

def update_user_push(user_id, field, value):
    return get_users_collection().update_one(
        {"_id": user_id},
        {"$push": {field: value}}
    )

def update_user_pull(user_id, field, value):
    return get_users_collection().update_one(
        {"_id": user_id},
        {"$pull": {field: value}}
    )