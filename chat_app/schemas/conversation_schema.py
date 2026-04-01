from datetime import datetime

def create_conversation_document(user1_id, user2_id):
    return {
        "participants": [user1_id, user2_id],
        "created_at": datetime.utcnow(),
        "last_message_at": datetime.utcnow()
    }