from datetime import datetime

def create_user_document(username, email, password, full_name):
    return {
        "username": username,
        "email": email,
        "password": password,
        "full_name": full_name,
        "created_at": datetime.utcnow(),
        "friends": [],
        "friend_requests_sent": [],
        "friend_requests_received": [],
        "status": "active"
    }