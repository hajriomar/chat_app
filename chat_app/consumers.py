import json
from channels.generic.websocket import AsyncWebsocketConsumer
from chat_app.repositories.message_repository import save_message
from chat_app.repositories.conversation_repository import update_last_message
from chat_app.schemas.message_schema import create_message_document
from chat_app.repositories.user_repository import get_user_by_username
from chat_app.services.spam_service import is_rate_limited
from bson import ObjectId
from channels.db import database_sync_to_async


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"
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

            msg_doc["sender_username"] = sender_username
            save_message(msg_doc)
            update_last_message(ObjectId(conversation_id))

    @database_sync_to_async
    def check_spam(self, sender_username):
        return is_rate_limited(sender_username, action="message", limit=5, window=10)

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            message = data.get("message", "").strip()
            sender = data.get("sender", "").strip()

            if not message:
                await self.send(text_data=json.dumps({
                    "type": "error",
                    "message": "Le message est vide."
                }))
                return

            if not sender:
                await self.send(text_data=json.dumps({
                    "type": "error",
                    "message": "Sender manquant."
                }))
                return

            # Vérification anti-spam Redis
            is_blocked = await self.check_spam(sender)
            print(f"[CONSUMER] sender={sender}, blocked={is_blocked}")
            if is_blocked:
                await self.send(text_data=json.dumps({
                    "type": "error",
                    "message": "Trop de messages envoyés. Attends quelques secondes."
                }))
                return

            # Sauvegarde MongoDB
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

        except Exception as e:
            await self.send(text_data=json.dumps({
                "type": "error",
                "message": f"Erreur serveur : {str(e)}"
            }))

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "type": "chat",
            "message": event["message"],
            "sender": event["sender"]
        }))