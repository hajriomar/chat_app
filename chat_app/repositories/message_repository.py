<<<<<<< HEAD
from bson import ObjectId
from chat_app.db.mongo import get_messages_collection
=======
from chat_app.db.mongo import messages_collection, conversations_collection, users_collection
from bson.objectid import ObjectId

>>>>>>> mariem

def save_message(message_doc):
    return get_messages_collection().insert_one(message_doc)

def get_messages_by_conversation(conversation_id):
    return list(
<<<<<<< HEAD
        get_messages_collection().find(
            {"conversation_id": ObjectId(conversation_id)}
=======
        messages_collection.find(
            {"conversation_id": ObjectId(conversation_id)} # Force la conversion en ObjectId
>>>>>>> mariem
        ).sort("timestamp", 1)
    )

def get_most_active_users(limit=3):
    """Trouve les utilisateurs qui envoient le plus de messages"""
    pipeline = [
        {"$group": {"_id": "$sender_username", "message_count": {"$sum": 1}}},
        {"$sort": {"message_count": -1}},
        {"$limit": limit}
    ]
    results = list(messages_collection.aggregate(pipeline))
    return [{"username": r["_id"], "count": r["message_count"]} for r in results if r["_id"]]

def get_most_solicited_users(limit=3):
    pipeline = [
        {"$unwind": "$participants"},
        {"$group": {"_id": "$participants", "conv_count": {"$sum": 1}}},
        {"$sort": {"conv_count": -1}},
        {"$limit": limit}
    ]
    results = list(conversations_collection.aggregate(pipeline))
    output = []
    for r in results:
        user = users_collection.find_one({"_id": r["_id"]})
        username = user["username"] if user else str(r["_id"])
        output.append({"user_id": username, "count": r["conv_count"]})
    return output

def get_groups_and_members():
    """Récupère la liste des groupes et leurs membres associés"""
    # On ne prend que les conversations qui ont un 'group_name' (donc les groupes)
    groups = conversations_collection.find({"group_name": {"$exists": True}})
    result = []
    for g in groups:
        member_names = []
        for p in g["participants"]:
            user = users_collection.find_one({"_id": p})
            member_names.append(user["username"] if user else str(p))
        result.append({"name": g["group_name"], "members": member_names})
    return result