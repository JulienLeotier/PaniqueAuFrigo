"""
ASGI config for PaniqueAuFrigo project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter

import front.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "PaniqueAuFrigo.settings")

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': URLRouter(
      front.routing.websocket_urlpatterns
    ),
})
