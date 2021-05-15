from channels.consumer import SyncConsumer, AsyncConsumer
from asgiref.sync import async_to_sync, sync_to_async
from authentication.models import User

from .models import Thread, Message, ChatList
import json
from channels.db import database_sync_to_async


class ChatConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        me = self.scope['user']
        other_username = self.scope['url_route']['kwargs']['username']
        other_user = await sync_to_async(User.objects.get)(username=other_username)
        self.thread_obj = await sync_to_async(Thread.objects.get_or_create_personal_thread)(me, other_user)
        self.room_name = f'personal_thread_{self.thread_obj.id}'
        await self.channel_layer.group_add(self.room_name, self.channel_name)
        await self.update_friendlist(other_user)

        await self.send({
            'type': 'websocket.accept'
        })
    

    async def websocket_receive(self, event):
        msg = json.dumps({
            'text': event.get('text'),
            'username': self.scope['user'].username
        })
        await self.store_message(event.get('text'))

        await self.channel_layer.group_send(self.room_name,
                                            {
                                                'type': 'websocket.message',
                                                "text": msg
                                            }
                                            )

    async def websocket_message(self, event):
        await self.send({
            'type': 'websocket.send',
            "text": event["text"],
        }
        )

    async def websocket_disconnect(self, event):
        await self.channel_layer.group_discard(self.room_name, self.channel_name)

    @database_sync_to_async
    def store_message(self, text):
        Message.objects.create(thread=self.thread_obj,sender=self.scope['user'],text=text)

    @database_sync_to_async
    def update_friendlist(self, other_user):
        try:
            friendlist = ChatList.objects.get(user = self.scope['user'])
        except ChatList.DoesNotExist:
            friendlist = ChatList.objects.create(user = self.scope['user'])

        friendlist.friendlist.add(other_user)
        try:
            other_friendlist = ChatList.objects.get(user = other_user)
        except ChatList.DoesNotExist:
            other_friendlist = ChatList.objects.create(user = other_user)
        other_friendlist.friendlist.add(self.scope['user'])
