import json

from channels.generic.websocket import AsyncWebsocketConsumer


class ShopConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        await self.channel_layer.group_add(
            "shops",
            self.channel_name,
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            "shops",
            self.channel_name,
        )

    async def shop_updated(self, event):
        await self.send(
            text_data=json.dumps(event["shop"])
        )