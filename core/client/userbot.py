from telethon import TelegramClient
from telethon.sessions import StringSession
from .config import API_ID, API_HASH
from handlers.dispatcher import register_dispatcher


class UserBot:
    def __init__(self, session_string):
        self.session_string = session_string
        self.client = TelegramClient(
            StringSession(session_string),
            API_ID,
            API_HASH
        )
        self.me = None

    async def start(self):
        register_dispatcher(self.client)
        await self.client.run_until_disconnected()
