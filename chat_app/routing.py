# chat_app/routing.py
from django.urls import re_path
from chat_app.consumers import ChatConsumer

websocket_urlpatterns = [
    # On utilise [^/]+ pour être sûr de capturer tout l'ID MongoDB
    re_path(r"ws/chat/(?P<room_name>[^/]+)/$", ChatConsumer.as_asgi()),
]