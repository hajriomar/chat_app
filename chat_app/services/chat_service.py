from datetime import datetime
from chat_app.repositories.user_repository import get_user_by_username, get_users_by_ids
from chat_app.repositories.conversation_repository import (
    find_conversation_between,
    create_conversation,
    find_conversations_by_user_id,
)
from chat_app.schemas.conversation_schema import create_conversation_document
from bson import ObjectId



def get_user_conversations(username):
    user = get_user_by_username(username)
    if not user:
        raise ValueError("Utilisateur introuvable")

    conversations = find_conversations_by_user_id(user["_id"])

    result = []
    for conv in conversations:
        is_group = conv.get("is_group", False)

        if is_group:
            label = conv.get("group_name") or f"Groupe {str(conv['_id'])[:6]}"
        else:
            other_participants = [uid for uid in conv["participants"] if uid != user["_id"]]
            other_users = get_users_by_ids(other_participants)

            if other_users:
                label = other_users[0]["username"]
            else:
                label = f"Conversation {str(conv['_id'])}"

        result.append({
            "conversation_id": str(conv["_id"]),
            "label": label,
            "is_group": is_group
        })

    return result




def create_conversation_if_not_exists(user1_id, user2_id):
    conversation = find_conversation_between(user1_id, user2_id)

    if conversation:
        return conversation["_id"]

    conversation_doc = create_conversation_document(
        participant_ids=[user1_id, user2_id],
        is_group=False,
        created_by=user1_id
    )

    result = create_conversation(conversation_doc)
    return result.inserted_id


def create_group_conversation(creator_username, participants_usernames, group_name):
    creator = get_user_by_username(creator_username)
    if not creator:
        raise ValueError("Créateur introuvable")

    if not group_name or not group_name.strip():
        raise ValueError("Nom du groupe obligatoire")

    participant_ids = [creator["_id"]]

    for username in participants_usernames:
        user = get_user_by_username(username)
        if not user:
            raise ValueError(f"Utilisateur introuvable : {username}")

        if user["_id"] not in participant_ids:
            participant_ids.append(user["_id"])

    if len(participant_ids) < 3:
        raise ValueError("Un groupe doit contenir au moins 3 membres")

    conversation_doc = create_conversation_document(
        participant_ids=participant_ids,
        is_group=True,
        group_name=group_name.strip(),
        created_by=creator["_id"]
    )

    result = create_conversation(conversation_doc)
    return result.inserted_id
