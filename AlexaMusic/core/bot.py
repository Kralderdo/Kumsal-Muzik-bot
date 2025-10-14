import os
from pyrogram import Client

# Heroku ortam değişkenlerinden bilgileri al
API_ID = int(os.getenv("API_ID", 0))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Botu başlat
AlexaBot = Client(
    "AlexaMusic",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
)
