from django.conf import settings
from pymongo import MongoClient

_client = None
_db = None

def get_client():
    global _client
    if _client is None:
        _client = MongoClient(settings.MONGO_URI)
    return _client

def get_db():
    global _db
    if _db is None:
        _db = get_client()[settings.MONGO_DB_NAME]
    return _db

def get_users_collection():
    return get_db()["users"]

def get_conversations_collection():
    return get_db()["conversations"]

def get_messages_collection():
    return get_db()["messages"]