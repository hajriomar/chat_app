from datetime import datetime
from chat_app.db.mongo import conversations_collection

def find_conversation_between(user1_id, user2_id):
    return conversations_collection.find_one({
        "participants": {"$all": [user1_id, user2_id], "$size": 2},
        "is_group": False
    })

def create_conversation(conversation_doc):
    return conversations_collection.insert_one(conversation_doc)

def find_conversations_by_user_id(user_id):
    return list(conversations_collection.find({
        "participants": user_id
    }))

def update_last_message(conversation_id):
    conversations_collection.update_one(
        {"_id": conversation_id},
        {"$set": {"last_message_at": datetime.utcnow()}}
    )