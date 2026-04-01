from pymongo import MongoClient
from django.conf import settings

client = MongoClient(settings.MONGO_URI)
db = client[settings.MONGO_DB_NAME]

users_collection = db["users"]
conversations_collection = db["conversations"]
messages_collection = db["messages"]