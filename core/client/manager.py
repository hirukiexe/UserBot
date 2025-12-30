import asyncio
import hashlib
from .userbot import UserBot

# session_hash : UserBot
userbots = {}


def session_fingerprint(session_string: str) -> str:
    # short unique fingerprint (safe)
    return hashlib.sha256(session_string.encode()).hexdigest()


async def start_userbot(session_string: str):
    fp = session_fingerprint(session_string)

    # 🔒 ALREADY RUNNING → DO NOTHING
    if fp in userbots:
        bot = userbots[fp]
        me = bot.me

        return {
            "already": True,
            "user_id": me.id,
            "first_name": me.first_name,
            "phone": me.phone,
            "dc_id": bot.client.session.dc_id
        }

    # ❗ Only now create client
    bot = UserBot(session_string)

    await bot.client.connect()

    if not await bot.client.is_user_authorized():
        await bot.client.disconnect()
        raise Exception("Invalid or expired session")

    me = await bot.client.get_me()
    bot.me = me

    # ✅ STORE BEFORE RUNNING
    userbots[fp] = bot

    # background run
    asyncio.create_task(bot.start())

    return {
        "already": False,
        "user_id": me.id,
        "first_name": me.first_name,
        "phone": me.phone,
        "dc_id": bot.client.session.dc_id
    }
