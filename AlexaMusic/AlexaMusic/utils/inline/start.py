# Copyright (C) 2024 by Alexa_Help @ Github
# Düzenlenmiş sürüm © 2025 Kralderdo (Derdo)

from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Bot ve owner bilgileri
BOT_USERNAME = "prenses_muzik_bot"
OWNER_LINK = "https://t.me/derveder"


# 🎵 Grup için start paneli
async def start_pannel(_):
    return [
        [
            InlineKeyboardButton(
                text="🎧 Komutlar", url=f"https://t.me/{BOT_USERNAME}?start=help"
            ),
            InlineKeyboardButton(text="👑 Owner", url=OWNER_LINK),
        ],
        [
            InlineKeyboardButton(text="🎵 Kanal", url=OWNER_LINK),
        ],
    ]


# 💬 Özel mesaj için start paneli
async def private_panel(_, username, OWNER):
    return [
        [
            InlineKeyboardButton(
                text="🎧 Komutlar", url=f"https://t.me/{BOT_USERNAME}?start=help"
            ),
            InlineKeyboardButton(text="👑 Owner", url=OWNER_LINK),
        ],
        [
            InlineKeyboardButton(text="🎵 Kanal", url=OWNER_LINK),
        ],
    ]
