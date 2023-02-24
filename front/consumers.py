# chat/consumers.py

import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from perso.models import Perso


class WsConsumers(WebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.perso_name = None
        self.perso_group_name = None
        self.perso = None

    def connect(self):
        self.perso_name = self.scope['url_route']['kwargs']['perso_name']  # get the perso name from the url
        self.perso_group_name = f'chat_{self.perso_name}'  # create the perso group name
        self.perso = Perso.objects.get(slug_name=self.perso_name)

        # connection has to be accepted
        self.accept()

        # join the room group
        async_to_sync(self.channel_layer.group_add)(
            self.perso_group_name,
            self.channel_name,
        )


    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.perso_group_name,
            self.channel_name,
        )

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # send chat message event to the room
        async_to_sync(self.channel_layer.group_send)(
            self.perso_group_name,
            {
                'type': 'chat_message',
                'message': message,
            }
        )

    def chat_message(self, event):
        self.send(text_data=json.dumps(event))
