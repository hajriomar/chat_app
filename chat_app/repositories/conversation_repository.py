from datetime import datetime
from bson import ObjectId
from chat_app.db.mongo import get_conversations_collection

def find_conversation_between(user1_id, user2_id):
<<<<<<< HEAD
    return get_conversations_collection().find_one({
        "participants": {"$all": [user1_id, user2_id], "$size": 2}
=======
    return conversations_collection.find_one({
        "participants": {"$all": [user1_id, user2_id], "$size": 2},
        "is_group": False
>>>>>>> mariem
    })

def create_conversation(conversation_doc):
    return get_conversations_collection().insert_one(conversation_doc)

def find_conversations_by_user_id(user_id):
    return list(get_conversations_collection().find({
        "participants": user_id
    }).sort("last_message_at", -1))

def find_conversation_by_id(conversation_id):
    return get_conversations_collection().find_one({
        "_id": ObjectId(conversation_id)
    })

def update_last_message(conversation_id):
    return get_conversations_collection().update_one(
        {"_id": ObjectId(conversation_id)},
        {"$set": {"last_message_at": datetime.utcnow()}}
    )