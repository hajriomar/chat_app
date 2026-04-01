from django.urls import path
from .views import (
    register_view,
    login_view,
    logout_view,
    online_users_view,
    login_page_view,
    online_friends_view,
    conversations_list_view,
    available_users_view,
    send_friend_request_view,
    received_requests_view,
    accept_friend_request_view,
)

urlpatterns = [
    path("register/", register_view),
    path("login/", login_view),
    path("login-page/", login_page_view),
    path("logout/", logout_view),
    path("online-users/", online_users_view),

    path("online-friends/", online_friends_view),
    path("conversations/", conversations_list_view),
    path("available-users/", available_users_view),
    path("send-friend-request/", send_friend_request_view),
    path("received-requests/", received_requests_view),
    path("accept-friend-request/", accept_friend_request_view),
]