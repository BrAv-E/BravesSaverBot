
import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.utils import executor
import yt_dlp

API_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start", "help"])
async def send_welcome(message: types.Message):
    await message.reply("🎧 Salom! Video link yuboring (YouTube, TikTok, Instagram) yoki qo‘shiq nomini yozing – sizga MP3 yoki video fayl yuboraman.")

@dp.message_handler(lambda message: message.text.startswith("http"))
async def handle_video_link(message: Message):
    url = message.text.strip()
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": "downloads/%(title)s.%(ext)s",
        "noplaylist": True,
        "quiet": True,
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info).replace(".webm", ".mp3").replace(".m4a", ".mp3")
        with open(filename, "rb") as audio:
            await message.reply_audio(audio, title=info.get("title", "Qo‘shiq"))
        os.remove(filename)
    except Exception as e:
        await message.reply(f"Xatolik: {str(e)}")

@dp.message_handler()
async def search_music(message: Message):
    query = message.text.strip()
    await message.reply("🔎 Qidirilmoqda... (bu funksiya test rejimida)")

if __name__ == "__main__":
    from os import makedirs
    makedirs("downloads", exist_ok=True)
    executor.start_polling(dp, skip_updates=True)
