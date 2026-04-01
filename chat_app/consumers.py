import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from chat_app.services.chat_service import create_message_in_conversation

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.conversation_id = self.scope["url_route"]["kwargs"]["conversation_id"]
        self.room_group_name = f"chat_{self.conversation_id}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)

            username = data.get("username")
            content = data.get("content")

            if not username or not content:
                await self.send(text_data=json.dumps({
                    "error": "username et content sont requis"
                }))
                return

            saved_message = await sync_to_async(create_message_in_conversation)(
                username,
                self.conversation_id,
                content
            )

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat_message",
                    "message": saved_message
                }
            )

        except Exception as e:
            await self.send(text_data=json.dumps({
                "error": str(e)
            }))

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event["message"]))