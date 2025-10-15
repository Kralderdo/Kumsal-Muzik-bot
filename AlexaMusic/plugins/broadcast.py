# Copyright (C) 2024 - Inflex Team
# Düzenlenmiş sürüm © 2025 Kralderdo (Derdo)

import asyncio
from pyrogram import filters
from pyrogram.enums import ChatMembersFilter
from pyrogram.errors import FloodWait

from InflexMusic import app
from InflexMusic.misc import SUDOERS
from InflexMusic.utils.database import (
    get_active_chats,
    get_authuser_names,
    get_client,
    get_served_chats,
    get_served_users,
)
from InflexMusic.utils.decorators.language import language
from InflexMusic.utils.formatters import alpha_to_int
from config import adminlist

# 🛰️ Broadcast durum değişkeni
IS_BROADCASTING = False


# ────────────────────────────────
# 🎙️ REKLAM / BROADCAST Komutu
# ────────────────────────────────
@app.on_message(filters.command(["reklam", "broadcast"]) & SUDOERS)
@language
async def broadcast_message(client, message, _):
    global IS_BROADCASTING

    if IS_BROADCASTING:
        return await message.reply_text("⚠️ Zaten bir broadcast işlemi devam ediyor.")

    if not message.reply_to_message and len(message.command) < 2:
        return await message.reply_text("<b>Kullanım:</b> /reklam [mesaj veya yanıtla]")

    # Mesaj türünü belirle
    if message.reply_to_message:
        if message.reply_to_message.photo:
            content_type = "photo"
            file_id = message.reply_to_message.photo.file_id
            caption = message.reply_to_message.caption or ""
        else:
            content_type = "text"
            text_content = message.reply_to_message.text
            caption = None
        reply_markup = getattr(message.reply_to_message, "reply_markup", None)
    else:
        content_type = "text"
        text_content = " ".join(message.command[1:])
        caption = None
        reply_markup = None

    IS_BROADCASTING = True
    await message.reply_text(_["broad_1"])

    # 🔸 Broadcast hedefleri belirleniyor
    to_chats = "-wfchat" in message.text or "-wfuser" in message.text or "-chat" in message.text
    to_users = "-wfuser" in message.text or "-user" in message.text
    to_assistants = "-assistant" in message.text

    total_sent = 0

    # ────────────────────────────────
    # 🏘️ Grup Yayını
    # ────────────────────────────────
    if to_chats or "-nobot" not in message.text:
        sent_chats = 0
        chats = [int(c["chat_id"]) for c in await get_served_chats()]
        for chat_id in chats:
            try:
                if content_type == "photo":
                    await app.send_photo(chat_id, photo=file_id, caption=caption, reply_markup=reply_markup)
                else:
                    await app.send_message(chat_id, text=text_content, reply_markup=reply_markup)
                sent_chats += 1
                total_sent += 1
                await asyncio.sleep(0.2)
            except FloodWait as fw:
                await asyncio.sleep(fw.value)
            except Exception:
                continue
        await message.reply_text(f"✅ {sent_chats} sohbet grubuna mesaj gönderildi.")

    # ────────────────────────────────
    # 👤 Kullanıcılara Yayın
    # ────────────────────────────────
    if to_users:
        sent_users = 0
        users = [int(u["user_id"]) for u in await get_served_users()]
        for user_id in users:
            try:
                if content_type == "photo":
                    await app.send_photo(user_id, photo=file_id, caption=caption, reply_markup=reply_markup)
                else:
                    await app.send_message(user_id, text=text_content, reply_markup=reply_markup)
                sent_users += 1
                total_sent += 1
                await asyncio.sleep(0.2)
            except FloodWait as fw:
                await asyncio.sleep(fw.value)
            except Exception:
                continue
        await message.reply_text(f"✅ {sent_users} kullanıcıya mesaj gönderildi.")

    # ────────────────────────────────
    # 🤖 Asistanlara Yayın
    # ────────────────────────────────
    if to_assistants:
        from InflexMusic.core.userbot import assistants
        await message.reply_text("📡 Asistanlar üzerinden yayın başlatılıyor...")
        text = ""
        for num in assistants:
            sent = 0
            client = await get_client(num)
            async for dialog in client.get_dialogs():
                try:
                    if content_type == "photo":
                        await client.send_photo(dialog.chat.id, photo=file_id, caption=caption)
                    else:
                        await client.send_message(dialog.chat.id, text=text_content)
                    sent += 1
                    total_sent += 1
                    await asyncio.sleep(3)
                except FloodWait as fw:
                    await asyncio.sleep(fw.value)
                except Exception:
                    continue
            text += f"✅ Asistan {num} → {sent} sohbet\n"
        await message.reply_text(text)

    IS_BROADCASTING = False
    await message.reply_text(f"🎯 Broadcast tamamlandı!\nToplam gönderilen: {total_sent}")


# ────────────────────────────────
# 🧹 Otomatik Yönetici Güncelleme
# ────────────────────────────────
async def auto_clean():
    while True:
        try:
            served_chats = await get_active_chats()
            for chat_id in served_chats:
                if chat_id not in adminlist:
                    adminlist[chat_id] = []
                    async for user in app.get_chat_members(chat_id, filter=ChatMembersFilter.ADMINISTRATORS):
                        if user.privileges and user.privileges.can_manage_video_chats:
                            adminlist[chat_id].append(user.user.id)
                    authusers = await get_authuser_names(chat_id)
                    for user in authusers:
                        user_id = await alpha_to_int(user)
                        adminlist[chat_id].append(user_id)
        except Exception:
            await asyncio.sleep(10)
        await asyncio.sleep(10)


asyncio.create_task(auto_clean())
