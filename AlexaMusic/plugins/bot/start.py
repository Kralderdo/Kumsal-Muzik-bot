# Copyright (C) 2024 by Alexa_Help @ Github
# Edited by @Kralderdo for Kumsal-Muzik-bot

import asyncio
from pyrogram import filters, Client
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from AlexaMusic import app
from AlexaMusic.utils.decorators.language import language

# OWNER listesi .env veya config.py'den geliyor
from config import OWNER_ID

# ----------------------------------------------------------
# Özel buton paneli
# ----------------------------------------------------------
def private_panel(_, username, owner_id):
    buttons = [
        [
            InlineKeyboardButton("🎶 Müzik Oynat", callback_data="open_play"),
            InlineKeyboardButton("📜 Komutlar", callback_data="help_menu")
        ],
        [
            InlineKeyboardButton("💬 Destek Grubu", url="https://t.me/sohbetpusulaa"),
            InlineKeyboardButton("📢 Kanal", url="https://t.me/TempoDestek")
        ],
        [
            InlineKeyboardButton("👑 Sahip", user_id=int(owner_id[0]) if isinstance(owner_id, list) else int(owner_id))
        ]
    ]
    return InlineKeyboardMarkup(buttons)


# ----------------------------------------------------------
# /start komutu
# ----------------------------------------------------------
@app.on_message(filters.command("start") & filters.private)
@language
async def start_comm(_, message, language):
    try:
        user = message.from_user
        username = user.username or user.first_name

        # private_panel artık await edilmiyor!
        out = private_panel(_, username, OWNER_ID)

        await message.reply_text(
            f"🎧 **Kumsal Müzik Bot'a Hoş Geldin {username}!**\n\n"
            "Ben Telegram gruplarında ve özel sohbetlerde müzik çalabilirim.\n"
            "Başlamak için menüden bir seçenek seç 💫",
            reply_markup=out
        )
    except Exception as e:
        await message.reply_text(f"⚠️ Bir hata oluştu:\n`{e}`")


# ----------------------------------------------------------
# Grup içi start mesajı
# ----------------------------------------------------------
@app.on_message(filters.command("start") & filters.group)
async def group_start(_, message):
    await message.reply_text(
        "🎵 **Kumsal Müzik aktif!**\n"
        "Sesli sohbette müzik çalmak için /play komutunu kullan.",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("📢 Destek Kanalı", url="https://t.me/TempoDestek")]]
        )
    )
