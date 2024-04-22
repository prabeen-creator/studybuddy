import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.apps import apps

Message= apps.get_model('studygroup','Message')

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chatroom_id = self.scope['url_route']['kwargs']['chatroom_id']
        self.chatroom_group_name = f'chat_{self.chatroom_id}'

        
        await self.channel_layer.group_add(
            self.chatroom_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        
        await self.channel_layer.group_discard(
            self.chatroom_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        
        # await Message.objects.create(
        #     content=message,
        #     sender= self.scope['user'],
        #     chatroom_id= self.chatroom_id
        # )

       
        await self.channel_layer.group_send(
            self.chatroom_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    async def chat_message(self, event):
        message = event['message']

       
        await self.send(text_data=json.dumps({
            'message': message
        }))
        
# class WebRTCSignalingConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.room_name = self.scope['url_route']['kwargs']['room_name']
#         self.room_group_name = 'chat_%s' % self.room_name

        
#         await self.channel_layer.group_add(
#             self.room_group_name,
#             self.channel_name
#         )

#         await self.accept()

#     async def disconnect(self, close_code):
        
#         await self.channel_layer.group_discard(
#             self.room_group_name,
#             self.channel_name
#         )

#     async def receive(self, text_data):
#         data = json.loads(text_data)
#         message_type = data.get('type')

#         if message_type == 'offer' or message_type == 'answer' or message_type == 'candidate':
            
#             await self.channel_layer.group_send(
#                 self.room_group_name,
#                 {
#                     'type': 'webrtc_message',
#                     'message': data
#                 }
#             )

#     async def webrtc_message(self, event):
        
#         message = event['message']
#         await self.send(text_data=json.dumps(message))