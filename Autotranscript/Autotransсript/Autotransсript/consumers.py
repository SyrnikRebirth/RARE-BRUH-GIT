from django.contrib.auth import get_user_model
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from chat.models import Message

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):

    async def fetch_messages(self, data):
        messages = Message.last_20_messeges()
        content = {
        'message': self.messages_to_json(messages)
        }
        self.send_message(content)

    async def new_message(self,data):
        auther = data['from']
        author_user =User.objects.filter(username=auther)[0]
        message = Message.objects.create(
        auther=author_user, content=data['message'])
        content = {
            'command': 'new_message',
            'message': self.message_to_json(message)
            }
        return self.send_chat_message(content)


    async def messages_to_json(self, messages):
        result = []
        for massage in messages:
            result.append[self.massage_to_json(massage)]
        return result

    async def message_to_json(self, message):
        return {
            'auther':message.auther.username,
            'content':message.content,
            'timestamp':str(message.timestamp)
        }



    commands = {'fetch_messages': fetch_messages,
    ' new_message': new_message}

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data['command']](self, data)

    async def send_chat_message(self,message):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    async def send_message(self, message):
        self.send(text_data=json.dumps({
            message
        }))

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            message
        }))
