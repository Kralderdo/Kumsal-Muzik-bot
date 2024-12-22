# Copyright (C) 2024 by Alexa_Help @ Github, < https://github.com/TheTeamAlexa >
# Subscribe On YT < Jankari Ki Duniya >. All rights reserved. © Alexa © Yukki.

""""
TheTeamAlexa is a project of Telegram bots with variety of purposes.
Copyright (c) 2024 -present Team=Alexa <https://github.com/TheTeamAlexa>

This program is free software: you can redistribute it and can modify
as you want or you can collabe if you have new ideas.
"""

import sys

from pyrogram import Client
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import BotCommand, BotCommandScopeAllPrivateChats, BotCommandScopeAllGroupChats

import config

from ..logging import LOGGER


private_commands = [
    BotCommand("start", "🎧 Botu başlatır"),
    BotCommand("yardim", "📖 Yardım menüsünü gösterir"),
]


group_commands = [
    BotCommand("oynat", "🔼 Müziği oynatır"),
    BotCommand("voynat", "📹 Videoyu oynatır"),
    BotCommand("atla", "⏭️ Sonraki Parçaya Geçer"),
    BotCommand("duraklat", "⏸️ Çalan Parçayı Durdurur"),
    BotCommand("devam", "▶️ Çalan Parçayı Devam Ettirir"),
    BotCommand("son", "⏹️ Çalan Parçayı Kapatır"),
    BotCommand("karistir", "🔀 Çalan Parçayı Karıştırır"),
    BotCommand("dongu", "🔄 Çalan Parçayı Tekrarlar"),
    BotCommand("sira", "📖 Çalma Listelerini Gösterir"),
    BotCommand("ilerisar", "⏩ Parçayı İleri Sarar"),
    BotCommand("gerisar", "⏪ Parçayı Geri Sarar"),
    BotCommand("playlist", "📖 Çalma Listenizi Gösterir"),
    BotCommand("bul", "📩 Seçtiğiniz Parçayı İndirir"),
    BotCommand("ayarlar", "⚙️ Bot Ayarlarını Gösterir"),
    BotCommand("restart", "🔃 Botu Yeniden Başlatır"),
    BotCommand("reload", "❤️‍🔥 Yönetici Önbelleğini Günceller"),

]

async def set_commands(client):

    await client.set_bot_commands(private_commands, scope=BotCommandScopeAllPrivateChats())


    await client.set_bot_commands(group_commands, scope=BotCommandScopeAllGroupChats())

class ArchMusic(Client):
    def __init__(self):
        LOGGER(__name__).info(f"Bot Başlatılıyor")
        super().__init__(
            "ArchMusic",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
        )

    async def start(self):
        await super().start()
        try:
            get_me = await self.get_me()
            self.username = get_me.username
            self.id = get_me.id

            video_url = "https://envs.sh/7cB.mp4"
            caption = "__kumsal aktif ✅. . . ⚡️__"

            try:
                await self.send_video(
                    config.LOG_GROUP_ID,
                    video=video_url,
                    caption=caption,
                )
            except:
                LOGGER(__name__).error(
                    "Bot log grubuna erişemedi. Log kanalınıza botunuzu eklediğinizden ve yönetici olarak terfi ettirdiğinizden emin olun!"
                )
                sys.exit()

            await set_commands(self)  


            a = await self.get_chat_member(config.LOG_GROUP_ID, self.id)
            if a.status != ChatMemberStatus.ADMINISTRATOR:
                LOGGER(__name__).error(
                    "Lütfen Logger Grubunda Botu Yönetici Olarak Terfi Ettirin"
                )
                sys.exit()

        except Exception as e:
            LOGGER(__name__).error(f"Bot başlatılırken hata oluştu: {e}")
            sys.exit()

        if get_me.last_name:
            self.name = get_me.first_name + " " + get_me.last_name
        else:
            self.name = get_me.first_name

        LOGGER(__name__).info(f"MusicBot {self.name} olarak başlatıldı")