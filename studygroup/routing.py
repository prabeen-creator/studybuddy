from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path, re_path
from channels.auth import AuthMiddlewareStack
from studygroup.consumers import ChatConsumer, WebRTCSignalingConsumer

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter([
            path('ws/chat/<int:chatroom_id>/', ChatConsumer.as_asgi()),
            re_path(r'ws/chat/(?P<room_name>\w+)/$', WebRTCSignalingConsumer.as_asgi()),
        ])
    ),
})