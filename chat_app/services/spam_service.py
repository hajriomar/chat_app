from chat_app.db.redis_client import redis_client
def is_rate_limited(username: str, action: str = "message", limit: int = 5, window: int = 10): 
    key = f"spam:{action}:{username}"
    count = redis_client.incr(key)
    # on met l'expiration seulement à la première création
    if count == 1:
        redis_client.expire(key, window)
        print(f"[REDIS SPAM] key={key}, count={count}, limit={limit}, window={window}")
    return count > limit