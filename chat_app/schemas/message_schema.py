from datetime import datetime
from bson import ObjectId

def create_message_document(conversation_id, sender_id, content):
    return {
        "conversation_id": ObjectId(conversation_id),
        "sender_id": sender_id,
        "content": content.strip(),
        "timestamp": datetime.utcnow()
    }