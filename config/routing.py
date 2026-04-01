# config/routing.py
from channels.routing import URLRouter
from chat_app.routing import websocket_urlpatterns as chat_ws

# Ici on pourrait combiner les routes de plusieurs apps
websocket_urlpatterns = chat_ws