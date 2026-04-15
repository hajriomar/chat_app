
from chat_app.repositories.redis_repository import (
    add_online_user, remove_online_user, get_online_users,
    increment_global_connections,log_global_activity
)
from datetime import datetime, timezone
from chat_app.db.redis_client import redis_client

def login_user(username):
    add_online_user(username)
    increment_global_connections()
    # Stocker l'heure de login pour calculer la durée plus tard
    login_time = datetime.now(timezone.utc).isoformat()
    redis_client.set(f"login_time:{username}", login_time)
    log_global_activity(username, "login")

def logout_user(username):
    remove_online_user(username)
    if username == "admin": return

    raw_login_time = redis_client.get(f"login_time:{username}")
    duration_str = None
 
    if raw_login_time:
        login_time_str = raw_login_time.decode('utf-8') if isinstance(raw_login_time, bytes) else raw_login_time
        login_dt = datetime.fromisoformat(login_time_str)
        delta = datetime.now(timezone.utc) - login_dt
        total_seconds = int(delta.total_seconds())
        
        # Formatage lisible
        minutes, seconds = divmod(total_seconds, 60)
        duration_str = f"{minutes}m {seconds}s"
 
        # Accumuler le temps total dans Redis
        redis_client.incrbyfloat(f"total_time:{username}", total_seconds)
        redis_client.delete(f"login_time:{username}")
 
    log_global_activity(username, "logout", duration=duration_str)

def list_online_users():
    return get_online_users()