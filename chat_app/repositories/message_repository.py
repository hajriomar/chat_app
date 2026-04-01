from bson import ObjectId
from chat_app.db.mongo import get_messages_collection

def save_message(message_doc):
    return get_messages_collection().insert_one(message_doc)

def get_messages_by_conversation(conversation_id):
    return list(
        get_messages_collection().find(
            {"conversation_id": ObjectId(conversation_id)}
        ).sort("timestamp", 1)
    )