from datetime import datetime
from chat_app.db.redis_client import redis_client
from datetime import datetime, timezone
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
    if username != "admin":
            increment_global_connections()
            log_global_activity(username, "login")

def remove_online_user(username):
    # On retire l'utilisateur de la liste des gens en ligne
    redis_client.srem(ONLINE_USERS_KEY, username)
    # On met son statut sur hors-ligne
    redis_client.set(f"user:{username}:status", "offline")
    # On ajoute juste la ligne de déconnexion dans son historique perso
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

def log_global_activity(username, event_type, duration=None):
    # event_type peut être "login" ou "logout"
    timestamp = datetime.utcnow().isoformat()
    
    # On ajoute la durée seulement si elle existe
    if duration:
        log_entry = f"{username}|{event_type}|{timestamp}|{duration}"
    else:
        log_entry = f"{username}|{event_type}|{timestamp}"
        
    # On stocke les 50 derniers événements mondiaux
    redis_client.lpush("global:activity:history", log_entry)
    redis_client.ltrim("global:activity:history", 0, 49)

#AJOUT
def get_global_activity_history():
    # Récupère les 50 dernières entrées
    activities = redis_client.lrange("global:activity:history", 0, 49)
    # Redis renvoie souvent des "bytes", on les décode en texte (UTF-8)
    return [act.decode('utf-8') if isinstance(act, bytes) else act for act in activities]

def get_all_users_total_time():
    """Récupère le temps total passé sur l'app pour chaque utilisateur (en secondes)"""
    keys = redis_client.keys("total_time:*")
    result = []
    for key in keys:
        key_str = key.decode('utf-8') if isinstance(key, bytes) else key
        username = key_str.replace("total_time:", "")
        raw_val = redis_client.get(key)
        total_seconds = int(float(raw_val)) if raw_val else 0
 
        # Formatage lisible
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
 
        if hours > 0:
            duration_str = f"{hours}h{minutes:02d}m"
        elif minutes > 0:
            duration_str = f"{minutes}m{seconds:02d}s"
        else:
            duration_str = f"{seconds}s"
 
        result.append({
            "username": username,
            "total_seconds": total_seconds,
            "duration": duration_str
        })
 
    # Trier par temps décroissant
    result.sort(key=lambda x: x["total_seconds"], reverse=True)
    return result
