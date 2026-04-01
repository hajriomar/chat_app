from datetime import datetime
from chat_app.db.redis_client import redis_client

ONLINE_USERS_KEY = "online_users"

def add_online_user(username):
    #Marquer l'utilisateur comme présent 
    redis_client.sadd(ONLINE_USERS_KEY, username)
    #Changer son statut individuel 
    redis_client.set(f"user:{username}:status", "online")
    #Ajouter à son historique personnel (List)
    redis_client.lpush(
        f"user:{username}:history",
        f"login:{datetime.utcnow().isoformat()}"
    )
    # On incrémente le compteur total de connexions du site
    increment_global_connections()
    # On enregistre l'événement dans le journal de bord général
    log_global_activity(username, "login")

def remove_online_user(username):
    redis_client.srem(ONLINE_USERS_KEY, username)
    redis_client.set(f"user:{username}:status", "offline")
    redis_client.lpush(
        f"user:{username}:history",
        f"logout:{datetime.utcnow().isoformat()}"
    )

def get_online_users():
    return list(redis_client.smembers(ONLINE_USERS_KEY))

#---- Historique et Statistiques REDIS ------
def get_user_history(username, limit=10):
    return redis_client.lrange(f"user:{username}:history", 0, limit - 1)

def increment_global_connections():
    # Incrémente un compteur global à chaque login
    redis_client.incr("stats:total_logins")

def get_total_logins():
    return redis_client.get("stats:total_logins") or 0

def log_global_activity(username, event_type):
    # event_type peut être "login" ou "logout"
    log_entry = f"{username}|{event_type}|{datetime.utcnow().isoformat()}"
    # On stocke les 50 derniers événements mondiaux
    redis_client.lpush("global:activity:history", log_entry)
    redis_client.ltrim("global:activity:history", 0, 49)