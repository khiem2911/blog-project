"""
ASGI config for project_social_network project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

from django.urls import path



from channels.routing import ProtocolTypeRouter, URLRouter

import app_social.routing

from channels.auth import AuthMiddlewareStack

from app_social.consumers import PersonalChatConsumer, OnlineStatusConsumer, NotificationConsumer


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_social_network.settings')


application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket":AuthMiddlewareStack(
        URLRouter(
            app_social.routing.websocket_urlpatterns
        )
    )
})