from datetime import datetime
from chat_app.repositories.user_repository import get_user_by_username, get_users_by_ids
from chat_app.repositories.conversation_repository import (
    find_conversation_between,
    create_conversation,
    find_conversations_by_user_id,
)

def create_conversation_if_not_exists(user1_id, user2_id):
    conversation = find_conversation_between(user1_id, user2_id)

    if conversation:
        return conversation["_id"]

    conversation_doc = {
        "participants": [user1_id, user2_id],
        "created_at": datetime.utcnow(),
        "last_message_at": datetime.utcnow()
    }

    result = create_conversation(conversation_doc)
    return result.inserted_id

def get_user_conversations(username):
    user = get_user_by_username(username)
    if not user:
        raise ValueError("Utilisateur introuvable")

    conversations = find_conversations_by_user_id(user["_id"])

    result = []
    for conv in conversations:
        other_participants = [uid for uid in conv["participants"] if uid != user["_id"]]
        other_users = get_users_by_ids(other_participants)

        if other_users:
            label = other_users[0]["username"]
        else:
            label = f"Conversation {str(conv['_id'])}"

        result.append({
            "conversation_id": str(conv["_id"]),
            "label": label
        })

    return result