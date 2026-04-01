from chat_app.db.mongo import messages_collection
from bson.objectid import ObjectId


def save_message(message_doc):
    return messages_collection.insert_one(message_doc)

def get_messages_by_conversation(conversation_id):
    return list(
        messages_collection.find(
            {"conversation_id": ObjectId(conversation_id)} # Force la conversion en ObjectId
        ).sort("timestamp", 1)
    )