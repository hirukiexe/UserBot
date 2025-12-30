import os

BOT_NAME = os.getenv("BOT_NAME", "daisy")
BOT_TOKEN = os.getenv("BOT_TOKEN")
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")

if not BOT_TOKEN or not API_ID or not API_HASH:
    raise ValueError("Environment variables missing")
