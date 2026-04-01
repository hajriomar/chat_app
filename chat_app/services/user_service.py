from chat_app.schemas.user_schema import create_user_document
from chat_app.repositories.user_repository import (
    create_user,
    get_user_by_username,
    get_users_by_ids,
    get_all_users_except,
    update_user_push,
    update_user_pull,
)
from chat_app.repositories.redis_repository import get_online_users
from chat_app.services.chat_service import create_conversation_if_not_exists

def register_user(username, email, password, full_name):
    existing_user = get_user_by_username(username)
    if existing_user:
        raise ValueError("Nom d'utilisateur déjà existant")

    user_doc = create_user_document(username, email, password, full_name)
    result = create_user(user_doc)
    return str(result.inserted_id)

def authenticate_user(username, password):
    user = get_user_by_username(username)

    if not user:
        raise ValueError("Utilisateur introuvable")

    if user["password"] != password:
        raise ValueError("Mot de passe incorrect")

    return user

def get_online_friends_for_user(username):
    current_user = get_user_by_username(username)
    if not current_user:
        raise ValueError("Utilisateur introuvable")

    online_usernames = get_online_users()
    friend_ids = current_user.get("friends", [])

    friends = get_users_by_ids(friend_ids)

    result = []
    for friend in friends:
        if friend["username"] in online_usernames:
            result.append({
                "username": friend["username"]
            })

    return result

def get_available_users_for_invitation(username):
    current_user = get_user_by_username(username)
    if not current_user:
        raise ValueError("Utilisateur introuvable")

    all_users = get_all_users_except(username)

    friend_ids = set(current_user.get("friends", []))
    sent_ids = set(current_user.get("friend_requests_sent", []))
    received_ids = set(current_user.get("friend_requests_received", []))

    excluded_ids = friend_ids.union(sent_ids).union(received_ids)

    available = []
    for user in all_users:
        if user["_id"] not in excluded_ids:
            available.append({
                "username": user["username"]
            })

    return available

def send_friend_request(sender_username, receiver_username):
    if sender_username == receiver_username:
        raise ValueError("Impossible de s'inviter soi-même")

    sender = get_user_by_username(sender_username)
    receiver = get_user_by_username(receiver_username)

    if not sender or not receiver:
        raise ValueError("Utilisateur introuvable")

    if receiver["_id"] in sender.get("friends", []):
        raise ValueError("Cet utilisateur est déjà votre ami")

    if receiver["_id"] in sender.get("friend_requests_sent", []):
        raise ValueError("Invitation déjà envoyée")

    if sender["_id"] in receiver.get("friend_requests_received", []):
        raise ValueError("Invitation déjà en attente")

    update_user_push(sender["_id"], "friend_requests_sent", receiver["_id"])
    update_user_push(receiver["_id"], "friend_requests_received", sender["_id"])

def get_received_friend_requests(username):
    current_user = get_user_by_username(username)
    if not current_user:
        raise ValueError("Utilisateur introuvable")

    sender_ids = current_user.get("friend_requests_received", [])
    senders = get_users_by_ids(sender_ids)

    result = []
    for user in senders:
        result.append({
            "username": user["username"]
        })

    return result

def accept_friend_request(current_username, sender_username):
    current_user = get_user_by_username(current_username)
    sender_user = get_user_by_username(sender_username)

    if not current_user or not sender_user:
        raise ValueError("Utilisateur introuvable")

    if sender_user["_id"] not in current_user.get("friend_requests_received", []):
        raise ValueError("Aucune invitation reçue de cet utilisateur")

    update_user_pull(current_user["_id"], "friend_requests_received", sender_user["_id"])
    update_user_pull(sender_user["_id"], "friend_requests_sent", current_user["_id"])

    update_user_push(current_user["_id"], "friends", sender_user["_id"])
    update_user_push(sender_user["_id"], "friends", current_user["_id"])

    create_conversation_if_not_exists(current_user["_id"], sender_user["_id"])