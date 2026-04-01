from datetime import datetime

def create_message_document(conversation_id, sender_id, content):
    return {
        "conversation_id": conversation_id,
        "sender": sender_id,
        "content": content,
        "timestamp": datetime.utcnow()
    }