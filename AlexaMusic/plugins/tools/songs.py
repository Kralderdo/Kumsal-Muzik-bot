# -*- coding: utf-8 -*-
# AlexaMusic yt-dlp Cookie Destekli İndirici
# Düzenleyen © 2025 Kralderdo (Derdo)

import os
import yt_dlp
from yt_dlp.utils import DownloadError

# Çerez dosyası yolu (önce Config Vars, sonra local fallback)
COOKIES_FILE = os.getenv("YT_COOKIES", "cookies/cookies.txt")

# Ana indirme ayarları
YDL_OPTS = {
    "quiet": True,
    "format": "bestaudio/best",
    "cookiefile": COOKIES_FILE if os.path.exists(COOKIES_FILE) else None,
    "outtmpl": "%(title)s.%(ext)s",
    "noplaylist": True,
    "nocheckcertificate": True,
    "geo_bypass": True,
    "ignoreerrors": True,
    "postprocessors": [
        {
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }
    ],
}


def download_youtube_audio(url, output_path="downloads"):
    """
    YouTube'dan MP3 olarak müzik indirir.
    Cookie desteği ile premium/girişli videolarda da çalışır.
    """
    os.makedirs(output_path, exist_ok=True)
    file_path = None

    try:
        with yt_dlp.YoutubeDL(YDL_OPTS) as ydl:
            info = ydl.extract_info(url, download=True)
            if info:
                filename = ydl.prepare_filename(info)
                file_path = filename.rsplit(".", 1)[0] + ".mp3"
    except DownloadError as e:
        print(f"[yt-dlp] Hata: {e}")
    except Exception as e:
        print(f"[!] Genel hata oluştu: {e}")

    return file_path


if __name__ == "__main__":
    test_url = input("🎵 YouTube Linki: ")
    path = download_youtube_audio(test_url)
    if path:
        print(f"✅ İndirme tamamlandı: {path}")
    else:
        print("❌ İndirme başarısız oldu.")
