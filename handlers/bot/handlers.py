from telethon import events
from core.events import command
from .handles import (
    send_ads
)


def register(bot):
    
    @bot.on(events.NewMessage(pattern=command.pattern("send")))
    async def start_handler(event):
        await send_ads.handle(event)
        
