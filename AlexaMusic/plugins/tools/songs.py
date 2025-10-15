# Copyright (C) 2024 by Alexa_Help @ Github
# Düzenlenmiş sürüm © 2025 Kralderdo (Derdo)

import os
import re
import yt_dlp
from pykeyboard import InlineKeyboard
from pyrogram import enums, filters
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InputMediaAudio,
    InputMediaVideo,
    Message,
)

from config import BANNED_USERS, SONG_DOWNLOAD_DURATION, SONG_DOWNLOAD_DURATION_LIMIT
from strings import get_command
from AlexaMusic import YouTube, app
from AlexaMusic.utils.decorators.language import language, languageCB
from AlexaMusic.utils.formatters import convert_bytes
from AlexaMusic.utils.inline.song import song_markup

# Sabit bilgiler
SONG_COMMAND = get_command("SONG_COMMAND")
BOT_USERNAME = "prenses_muzik_bot"
OWNER_LINK = "https://t.me/derveder"


# ────────────────────────────────
# 🎵 Grup Komutu
# ────────────────────────────────
@app.on_message(filters.command(SONG_COMMAND) & filters.group & ~BANNED_USERS)
@language
async def song_commad_group(client, message: Message, _):
    upl = InlineKeyboardMarkup(
        [[
            InlineKeyboardButton(
                text=_["SG_B_1"],
                url=f"https://t.me/{BOT_USERNAME}?start=song",
            )
        ]]
    )
    await message.reply_text(_["song_1"], reply_markup=upl)


# ────────────────────────────────
# 🎧 Özel Mesaj Komutu
# ────────────────────────────────
@app.on_message(filters.command(SONG_COMMAND) & filters.private & ~BANNED_USERS)
@language
async def song_commad_private(client, message: Message, _):
    await message.delete()
    url = await YouTube.url(message)
    if url:
        if not await YouTube.exists(url):
            return await message.reply_text(_["song_5"])
        mystic = await message.reply_text(_["play_1"])
        title, duration_min, duration_sec, thumbnail, vidid = await YouTube.details(url)
        if str(duration_min) == "None":
            return await mystic.edit_text(_["song_3"])
        if int(duration_sec) > SONG_DOWNLOAD_DURATION_LIMIT:
            return await mystic.edit_text(
                _["play_4"].format(SONG_DOWNLOAD_DURATION, duration_min)
            )
        buttons = song_markup(_, vidid)
        await mystic.delete()
        return await message.reply_photo(
            thumbnail or "assets/default.jpg",
            caption=_["song_4"].format(title),
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    else:
        if len(message.command) < 2:
            return await message.reply_text(_["song_2"])

    mystic = await message.reply_text(_["play_1"])
    query = message.text.split(None, 1)[1]
    try:
        title, duration_min, duration_sec, thumbnail, vidid = await YouTube.details(query)
    except:
        return await mystic.edit_text(_["play_3"])
    if str(duration_min) == "None":
        return await mystic.edit_text(_["song_3"])
    if int(duration_sec) > SONG_DOWNLOAD_DURATION_LIMIT:
        return await mystic.edit_text(
            _["play_6"].format(SONG_DOWNLOAD_DURATION, duration_min)
        )
    buttons = song_markup(_, vidid)
    await mystic.delete()
    return await message.reply_photo(
        thumbnail or "assets/default.jpg",
        caption=_["song_4"].format(title),
        reply_markup=InlineKeyboardMarkup(buttons),
    )


# ────────────────────────────────
# 🔙 Geri Dön Butonu
# ────────────────────────────────
@app.on_callback_query(filters.regex(pattern=r"song_back") & ~BANNED_USERS)
@languageCB
async def songs_back_helper(client, CallbackQuery, _):
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    stype, vidid = callback_request.split("|")
    buttons = song_markup(_, vidid)
    return await CallbackQuery.edit_message_reply_markup(
        reply_markup=InlineKeyboardMarkup(buttons)
    )


# ────────────────────────────────
# 🎶 Kalite Seçim Butonları
# ────────────────────────────────
@app.on_callback_query(filters.regex(pattern=r"song_helper") & ~BANNED_USERS)
@languageCB
async def song_helper_cb(client, CallbackQuery, _):
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    stype, vidid = callback_request.split("|")
    try:
        await CallbackQuery.answer(_["song_6"], show_alert=True)
    except:
        pass

    try:
        formats_available, link = await YouTube.formats(vidid, True)
    except:
        return await CallbackQuery.edit_message_text(_["song_7"])

    keyboard = InlineKeyboard()
    done = []

    if stype == "audio":
        for x in formats_available:
            check = x["format"]
            if "audio" in check and x["filesize"]:
                form = x["format_note"].title()
                if form in done:
                    continue
                done.append(form)
                sz = convert_bytes(x["filesize"])
                fom = x["format_id"]
                keyboard.row(
                    InlineKeyboardButton(
                        text=f"{form} Kalite • {sz}",
                        callback_data=f"song_download {stype}|{fom}|{vidid}",
                    ),
                )
    else:
        done = [160, 133, 134, 135, 136, 137, 298, 299, 264, 304, 266]
        for x in formats_available:
            if x["filesize"] and int(x["format_id"]) in done:
                sz = convert_bytes(x["filesize"])
                ap = x["format"].split("-")[1]
                keyboard.row(
                    InlineKeyboardButton(
                        text=f"{ap} • {sz}",
                        callback_data=f"song_download {stype}|{x['format_id']}|{vidid}",
                    )
                )

    keyboard.row(
        InlineKeyboardButton(text=_["BACK_BUTTON"], callback_data=f"song_back {stype}|{vidid}"),
        InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data=f"close"),
    )
    return await CallbackQuery.edit_message_reply_markup(reply_markup=keyboard)


# ────────────────────────────────
# ⬇️ Şarkı İndirme (Çerezli yt-dlp)
# ────────────────────────────────
@app.on_callback_query(filters.regex(pattern=r"song_download") & ~BANNED_USERS)
@languageCB
async def song_download_cb(client, CallbackQuery, _):
    try:
        await CallbackQuery.answer("İndiriliyor...")
    except:
        pass

    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    stype, format_id, vidid = callback_request.split("|")
    mystic = await CallbackQuery.edit_message_text(_["song_8"])
    yturl = f"https://www.youtube.com/watch?v={vidid}"

    # ✅ Çerezli yt-dlp ayarı
    cookies_file = os.getenv("YT_COOKIES", "cookies.txt")
    ydl_opts = {"quiet": True, "cookiefile": cookies_file}

    with yt_dlp.YoutubeDL(ydl_opts) as ytdl:
        x = ytdl.extract_info(yturl, download=False)

    title = (x["title"]).title()
    title = re.sub(r"\W+", " ", title)
    duration = x.get("duration", 0)
    performer = x.get("uploader", "YouTube")

    thumb_image_path = await CallbackQuery.message.download() or "assets/default.jpg"

    if stype == "video":
        try:
            file_path = await YouTube.download(
                yturl, mystic, songvideo=True, format_id=format_id, title=title
            )
        except Exception as e:
            return await mystic.edit_text(_["song_9"].format(e))

        med = InputMediaVideo(
            media=file_path,
            duration=duration,
            thumb=thumb_image_path,
            caption=title,
            supports_streaming=True,
        )
        await mystic.edit_text(_["song_11"])
        await app.send_chat_action(chat_id=CallbackQuery.message.chat.id, action=enums.ChatAction.UPLOAD_VIDEO)
        try:
            await CallbackQuery.edit_message_media(media=med)
        except Exception as e:
            print(e)
            return await mystic.edit_text(_["song_10"])
        os.remove(file_path)

    else:
        try:
            filename = await YouTube.download(
                yturl, mystic, songaudio=True, format_id=format_id, title=title
            )
        except Exception as e:
            return await mystic.edit_text(_["song_9"].format(e))

        med = InputMediaAudio(
            media=filename,
            caption=title,
            thumb=thumb_image_path,
            title=title,
            performer=performer,
        )
        await mystic.edit_text(_["song_11"])
        await app.send_chat_action(chat_id=CallbackQuery.message.chat.id, action=enums.ChatAction.UPLOAD_AUDIO)
        try:
            await CallbackQuery.edit_message_media(media=med)
        except Exception as e:
            print(e)
            return await mystic.edit_text(_["song_10"])
        os.remove(filename)
