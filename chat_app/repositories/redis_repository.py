from datetime import datetime
from chat_app.db.redis_client import redis_client

ONLINE_USERS_KEY = "online_users"

def add_online_user(username):
    redis_client.sadd(ONLINE_USERS_KEY, username)
    redis_client.set(f"user:{username}:status", "online")
    redis_client.lpush(
        f"user:{username}:history",
        f"login:{datetime.utcnow().isoformat()}"
    )

def remove_online_user(username):
    redis_client.srem(ONLINE_USERS_KEY, username)
    redis_client.set(f"user:{username}:status", "offline")
    redis_client.lpush(
        f"user:{username}:history",
        f"logout:{datetime.utcnow().isoformat()}"
    )

def get_online_users():
    return list(redis_client.smembers(ONLINE_USERS_KEY))

def get_user_history(username, limit=10):
    return redis_client.lrange(f"user:{username}:history", 0, limit - 1)