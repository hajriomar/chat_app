from chat_app.schemas.conversation_schema import create_conversation_document
from chat_app.schemas.message_schema import create_message_document

from chat_app.repositories.user_repository import (
    get_user_by_username,
    get_users_by_ids,
    get_user_by_id,
)
from chat_app.repositories.conversation_repository import (
    find_conversation_between,
    create_conversation,
    find_conversations_by_user_id,
    find_conversation_by_id,
    update_last_message,
)
from chat_app.repositories.message_repository import (
    save_message,
    get_messages_by_conversation,
)

def create_conversation_if_not_exists(user1_id, user2_id):
    conversation = find_conversation_between(user1_id, user2_id)

    if conversation:
        return conversation["_id"]

    conversation_doc = create_conversation_document(user1_id, user2_id)
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
            "label": label,
            "last_message_at": conv.get("last_message_at").isoformat() if conv.get("last_message_at") else None
        })

    return result

def get_conversation_messages(username, conversation_id):
    user = get_user_by_username(username)
    if not user:
        raise ValueError("Utilisateur introuvable")

    conversation = find_conversation_by_id(conversation_id)
    if not conversation:
        raise ValueError("Conversation introuvable")

    if user["_id"] not in conversation.get("participants", []):
        raise ValueError("Accès interdit à cette conversation")

    messages = get_messages_by_conversation(conversation_id)

    result = []
    for msg in messages:
        sender = get_user_by_id(msg["sender_id"])

        result.append({
            "message_id": str(msg["_id"]),
            "conversation_id": str(msg["conversation_id"]),
            "sender_username": sender["username"] if sender else "unknown",
            "content": msg["content"],
            "timestamp": msg["timestamp"].isoformat() if msg.get("timestamp") else None
        })

    return result

def create_message_in_conversation(username, conversation_id, content):
    if not content or not content.strip():
        raise ValueError("Le message est vide")

    sender = get_user_by_username(username)
    if not sender:
        raise ValueError("Utilisateur introuvable")

    conversation = find_conversation_by_id(conversation_id)
    if not conversation:
        raise ValueError("Conversation introuvable")

    if sender["_id"] not in conversation.get("participants", []):
        raise ValueError("Accès interdit à cette conversation")

    message_doc = create_message_document(
        conversation_id=conversation_id,
        sender_id=sender["_id"],
        content=content
    )

    result = save_message(message_doc)
    update_last_message(conversation_id)

    return {
        "message_id": str(result.inserted_id),
        "conversation_id": conversation_id,
        "sender_username": username,
        "content": message_doc["content"],
        "timestamp": message_doc["timestamp"].isoformat()
    }