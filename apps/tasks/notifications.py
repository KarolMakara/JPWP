from channels.generic.websocket import AsyncWebsocketConsumer


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Add the WebSocket client to the 'notifications' group
        await self.channel_layer.group_add('notifications', self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Remove the WebSocket client from the 'notifications' group
        await self.channel_layer.group_discard('notifications', self.channel_name)

    async def notification(self, event):
        # Send the notification to the client-side
        message = event['message']
        await self.send(text_data=message)
