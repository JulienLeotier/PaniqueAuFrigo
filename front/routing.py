from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/notifications/(?P<perso_name>\w+)', consumers.WsConsumers.as_asgi()),
]
