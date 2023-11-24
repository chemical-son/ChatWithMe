import json

from channels.generic.websocket import AsyncWebsocketConsumer


from channels.db import database_sync_to_async

from django.contrib.auth import get_user_model
from django.utils import timezone

from .models import Room, Message


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        self.message = text_data_json["message"]

        # get username and room id to store message in message table
        self.username = self.scope["session"]["username"]
        self.room_id = self.scope["session"]["room_id"]

        #
        # get access to database and store messages
        await self.save_message()

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat.message",
                "message": self.message,
                "sender": self.username,
                "message_time": '"' + str(timezone.now()) + '"',
            },
        )

    # Receive message from room group
    async def chat_message(self, event):
        self.message = event["message"]
        self.sender = event["sender"]

        # Send message to WebSocket
        await self.send(
            text_data=json.dumps(
                {
                    "message": self.message,
                    "sender": self.sender,
                    "message_time": '"' + str(timezone.now()) + '"',
                }
            )
        )

    # get access to database and store messages
    @database_sync_to_async
    def save_message(self):
        user = get_user_model().objects.get(username=self.username)
        room = Room.objects.get(id=self.room_id)
        message_content = self.message

        m = Message.objects.create(sender=user, room=room, content=message_content)

        if m is None:
            print("::error in storing message in DB.")
