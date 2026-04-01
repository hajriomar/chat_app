from chat_app.db.mongo import users_collection

def create_user(user_doc):
    return users_collection.insert_one(user_doc)

def get_user_by_username(username):
    return users_collection.find_one({"username": username})

def get_user_by_id(user_id):
    return users_collection.find_one({"_id": user_id})

def get_all_users_except(username):
    return list(users_collection.find({"username": {"$ne": username}}))

def get_users_by_ids(user_ids):
    return list(users_collection.find({"_id": {"$in": user_ids}}))

def update_user_push(user_id, field, value):
    users_collection.update_one(
        {"_id": user_id},
        {"$addToSet": {field: value}}
    )
def update_user_pull(user_id, field, value):
    users_collection.update_one(
        {"_id": user_id},
        {"$pull": {field: value}}
    )