# Copyright (C) 2024 by Alexa_Help @ Github, < https://github.com/TheTeamAlexa >
# Subscribe On YT < Jankari Ki Duniya >. All rights reserved. © Alexa © Yukki.

"""
TheTeamAlexa is a project of Telegram bots with variety of purposes.
Copyright (c) 2024 -present Team Alexa.

This program is free software: you can redistribute it and can modify
as you want or you can collab if you have new ideas.
"""

import asyncio
from pyrogram import enums, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from youtubesearchpython.__future__ import VideosSearch

import config
from config import BANNED_USERS
from config.config import OWNER_ID
from strings import get_command, get_string
from AlexaMusic import Telegram, YouTube, app
from AlexaMusic.misc import SUDOERS
from AlexaMusic.plugins.play.playlist import del_plist_msg
from AlexaMusic.plugins.sudo.sudoers import sudoers_list
from AlexaMusic.utils.database import (
    add_served_chat,
    is_served_user,
    add_served_user,
    blacklisted_chats,
    get_assistant,
    get_lang,
    get_userss,
    is_on_off,
    is_served_private_chat,
)
from AlexaMusic.utils.decorators.language import LanguageStart
from AlexaMusic.utils.inline import help_pannel, private_panel, start_pannel
from AlexaMusic.utils.command import commandpro

loop = asyncio.get_running_loop()

CHANNEL_LINK = "https://t.me/sesizlikkkDusmanimizzzz"

@app.on_message(
    filters.command(get_command("START_COMMAND")) & filters.private & ~BANNED_USERS
)
@LanguageStart
async def start_comm(client, message: Message, _):
    await add_served_user(message.from_user.id)
    if len(message.text.split()) > 1:
        name = message.text.split(None, 1)[1]
        if name.startswith("help"):
            keyboard = help_pannel(_)
            return await message.reply_text(_["help_1"], reply_markup=keyboard)
        if name.startswith("song"):
            return await message.reply_text(_["song_2"])
        if name.startswith("sta"):
            m = await message.reply_text(
                f"🥱 Kişisel istatistikleriniz alınıyor {config.MUSIC_BOT_NAME} sunucusunda..."
            )
            stats = await get_userss(message.from_user.id)
            if not stats:
                await asyncio.sleep(1)
                return await m.edit(_["ustats_1"])

            def get_stats():
                msg = ""
                limit = 0
                results = {}
                for i in stats:
                    top_list = stats[i]["spot"]
                    results[str(i)] = top_list
                list_arranged = dict(
                    sorted(results.items(), key=lambda item: item[1], reverse=True)
                )
                tota = 0
                videoid = None
                for vidid, count in list_arranged.items():
                    tota += count
                    if limit >= 10:
                        continue
                    if limit == 0:
                        videoid = vidid
                    limit += 1
                    details = stats.get(vidid)
                    title = (details["title"][:35]).title()
                    if vidid == "telegram":
                        msg += f"🔗[Telegram Medya]({CHANNEL_LINK}) **{count} kez çalındı.**\n\n"
                    else:
                        msg += f"🔗 [{title}](https://www.youtube.com/watch?v={vidid}) **{count} kez çalındı.**\n\n"
                msg = _["ustats_2"].format(len(stats), tota, limit) + msg
                return videoid, msg

            try:
                videoid, msg = await loop.run_in_executor(None, get_stats)
            except Exception as e:
                print(e)
                return
            thumbnail = await YouTube.thumbnail(videoid, True)
            if not thumbnail:
                thumbnail = "assets/default.jpg"
            await m.delete()
            await message.reply_photo(photo=thumbnail, caption=msg)
            return

        if name.startswith("sud"):
            await sudoers_list(client=client, message=message, _=_)
            if await is_on_off(config.LOG):
                sender_id = message.from_user.id
                sender_name = message.from_user.first_name
                return await app.send_message(
                    config.LOG_GROUP_ID,
                    f"{message.from_user.mention} bir sudo komutu başlattı.\n\n**ID:** {sender_id}\n**Ad:** {sender_name}",
                )
            return

        if name.startswith("lyr"):
            query = str(name).replace("lyrics_", "", 1)
            lyrical = config.lyrical
            lyrics = lyrical.get(query)
            if lyrics:
                return await Telegram.send_split_text(message, lyrics)
            else:
                return await message.reply_text("Şarkı sözleri alınamadı.")

        if name.startswith("del"):
            await del_plist_msg(client=client, message=message, _=_)

        if name.startswith("inf"):
            m = await message.reply_text("🔎 Bilgi getiriliyor...")
            query = (str(name)).replace("info_", "", 1)
            query = f"https://www.youtube.com/watch?v={query}"
            results = VideosSearch(query, limit=1)
            for result in (await results.next())["result"]:
                title = result["title"]
                duration = result["duration"]
                views = result["viewCount"]["short"]
                thumbnail = result["thumbnails"][0]["url"].split("?")[0]
                channel = result["channel"]["name"]
                link = result["link"]
                published = result["publishedTime"]

            searched_text = f"""
😲 **Parça Bilgisi**

📌 **Başlık:** {title}
⏳ **Süre:** {duration}
👀 **Görüntülenme:** {views}
⏰ **Yayın:** {published}
🎥 **Kanal:** {channel}
🔗 **Bağlantı:** [Dinle]({link})

💖 Güç: [{config.MUSIC_BOT_NAME}]({CHANNEL_LINK})
"""
            key = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="🎧 Dinle", url=link),
                        InlineKeyboardButton(text="Kapat", callback_data="close"),
                    ],
                ]
            )
            await m.delete()
            await app.send_photo(
                message.chat.id,
                photo=thumbnail,
                caption=searched_text,
                parse_mode=enums.ParseMode.MARKDOWN,
                reply_markup=key,
            )

    else:
        try:
            await app.resolve_peer(OWNER_ID[0])
            OWNER = OWNER_ID[0]
        except:
            OWNER = None

        me = await app.get_me()
        username = me.username or config.MUSIC_BOT_NAME
        out = private_panel(_, username, OWNER)

        if config.START_IMG_URL:
            try:
                await message.reply_photo(
                    photo=config.START_IMG_URL,
                    caption=_["start_2"].format(config.MUSIC_BOT_NAME),
                    reply_markup=InlineKeyboardMarkup(out),
                )
            except:
                await message.reply_text(
                    _["start_2"].format(config.MUSIC_BOT_NAME),
                    reply_markup=InlineKeyboardMarkup(out),
                )
        else:
            await message.reply_text(
                _["start_2"].format(config.MUSIC_BOT_NAME),
                reply_markup=InlineKeyboardMarkup(out),
            )
        if await is_on_off(config.LOG):
            sender_id = message.from_user.id
            sender_name = message.from_user.first_name
            await app.send_message(
                config.LOG_GROUP_ID,
                f"{message.from_user.mention} botu başlattı.\n\n**ID:** {sender_id}\n**Ad:** {sender_name}",
            )


@app.on_message(
    filters.command(get_command("START_COMMAND")) & filters.group & ~BANNED_USERS
)
@LanguageStart
async def testbot(client, message: Message, _):
    out = start_pannel(_)
    return await message.reply_text(
        _["start_1"].format(message.chat.title, config.MUSIC_BOT_NAME),
        reply_markup=InlineKeyboardMarkup(out),
    )


welcome_group = 2


@app.on_message(filters.new_chat_members, group=welcome_group)
async def welcome(client, message: Message):
    chat_id = message.chat.id
    if config.PRIVATE_BOT_MODE == str(True):
        if not await is_served_private_chat(message.chat.id):
            await message.reply_text(
                "**Özel Müzik Botu**\n\nBu bot sadece yetkili sohbetlerde çalışır. Yetkilendirme için [sahip](https://t.me/sesizlikkkDusmanimizzzz) ile iletişime geç."
            )
            return await app.leave_chat(message.chat.id)
    else:
        await add_served_chat(chat_id)
