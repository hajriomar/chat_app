from chat_app.repositories.redis_repository import (
    add_online_user,
    remove_online_user,
    get_online_users,
)

def login_user(username):
    add_online_user(username)

def logout_user(username):
    remove_online_user(username)

def list_online_users():
    return get_online_users()