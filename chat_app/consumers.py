import json
from channels.generic.websocket import AsyncWebsocketConsumer
<<<<<<< HEAD
from asgiref.sync import sync_to_async
from chat_app.services.chat_service import create_message_in_conversation

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.conversation_id = self.scope["url_route"]["kwargs"]["conversation_id"]
        self.room_group_name = f"chat_{self.conversation_id}"

=======
from chat_app.repositories.message_repository import save_message
from chat_app.repositories.conversation_repository import update_last_message
from chat_app.schemas.message_schema import create_message_document
from chat_app.repositories.user_repository import get_user_by_username
from bson import ObjectId
from channels.db import database_sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"
>>>>>>> mariem
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

    @database_sync_to_async
    def persist_message(self, conversation_id, sender_username, content):
        user = get_user_by_username(sender_username)
        if user:
            msg_doc = create_message_document(
                ObjectId(conversation_id), 
                user["_id"], 
                content
            )
            # Ajout du pseudo pour l'historique
            msg_doc["sender_username"] = sender_username
            save_message(msg_doc)
            update_last_message(ObjectId(conversation_id))

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)

<<<<<<< HEAD
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
=======
        # Sauvegarde
        await self.persist_message(self.room_name, sender, message)

        # Diffusion au groupe
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "sender": sender,
            }
        )

    async def chat_message(self, event):
        # Cette fonction est appelée une fois pour chaque utilisateur dans le groupe
        await self.send(text_data=json.dumps({
            "message": event["message"],
            "sender": event["sender"]
        }))
>>>>>>> mariem
