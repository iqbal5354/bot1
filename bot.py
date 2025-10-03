import os
import logging
from telethon import TelegramClient
from telethon.sessions import StringSession
from perintah import init as load_perintah
from perintah.addbot import load_token

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
SESSION = os.getenv("SESSION")

logging.info("🔍 Cek token dari .addbot ...")
BOT_TOKEN = load_token()

if BOT_TOKEN:
    logging.info("🤖 Bullove BOT starting...")
    client = TelegramClient("bot_session", API_ID, API_HASH).start(bot_token=BOT_TOKEN)
else:
    logging.info("🤖 Bullove Userbot starting...")
    client = TelegramClient(StringSession(SESSION), API_ID, API_HASH)


async def main():
    from tools import get_owner_id, check_mode

    try:
        logging.info("🔍 Mendapatkan owner id ...")
        owner_id, owner_name = await get_owner_id(client)
        logging.info(f"ℹ️ OWNER_ID otomatis diset ke: {owner_id} ({owner_name})")
    except Exception as e:
        logging.error(f"❌ Gagal mendapatkan owner id: {e}", exc_info=True)

    try:
        mode = check_mode(client)
        logging.info(f"🔧 Mode berjalan: {mode}")
    except Exception as e:
        logging.error(f"❌ Gagal cek mode: {e}", exc_info=True)

    # Load semua perintah via __init__.py
    logging.info("📂 Mulai load perintah...")
    load_perintah(client)

    logging.info("🚀 Semua modul berhasil dimuat, menunggu event ...")
    await client.run_until_disconnected()


if __name__ == "__main__":
    with client:
        client.loop.run_until_complete(main())
