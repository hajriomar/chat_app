
from django.urls import re_path
from chat_app.consumers import ChatConsumer
websocket_urlpatterns = [
re_path(r"ws/chat/(?P<room_name>[^/]+)/$", ChatConsumer.as_asgi()),
]

# config/routing.py
from channels.routing import URLRouter
from chat_app.routing import websocket_urlpatterns as chat_ws

# Ici on pourrait combiner les routes de plusieurs apps
websocket_urlpatterns = chat_ws

