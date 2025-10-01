import os
import importlib
import logging
from telethon import TelegramClient
from telethon.sessions import StringSession

# Setup logging
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# Ambil ENV
API_ID = int(os.getenv("API_ID", "0"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")  # Untuk BOT
SESSION = os.getenv("SESSION")      # Untuk Userbot

client = None
MODE = None

# Tentukan mode otomatis
if BOT_TOKEN:
    logging.info("🤖 Bullove BOT starting...")
    client = TelegramClient("bot_session", API_ID, API_HASH).start(bot_token=BOT_TOKEN)
    MODE = "BOT"
elif SESSION:
    logging.info("🤖 Bullove Userbot starting...")
    client = TelegramClient(StringSession(SESSION), API_ID, API_HASH)
    MODE = "USERBOT"
else:
    logging.error("❌ Tidak ada BOT_TOKEN atau SESSION di Railway Variables!")
    exit(1)


async def main():
    from tools import get_owner_id, check_mode

    # Cek identitas owner
    try:
        owner_id, owner_name = await get_owner_id(client)
        logging.info(f"ℹ️ OWNER_ID otomatis diset ke: {owner_id} ({owner_name})")
    except Exception as e:
        logging.error(f"❌ Gagal mendapatkan owner id: {e}", exc_info=True)

    # Cek mode
    try:
        mode = check_mode(client)
        logging.info(f"🔧 Mode berjalan: {mode}")
    except Exception as e:
        logging.error(f"❌ Gagal cek mode: {e}", exc_info=True)

    # Auto load semua modul di folder perintah
    logging.info("📂 Mulai load perintah...")
    for file in os.listdir("perintah"):
        if file.endswith(".py") and not file.startswith("__"):
            modulename = file[:-3]
            try:
                module = importlib.import_module(f"perintah.{modulename}")
                if hasattr(module, "init"):
                    module.init(client)
                if hasattr(module, "init_owner"):
                    await module.init_owner(client)
                logging.info(f"✅ Loaded {modulename}")
            except Exception as e:
                logging.error(f"❌ Gagal load {modulename}: {e}", exc_info=True)

    logging.info("🚀 Semua modul berhasil dimuat, menunggu event ...")
    await client.run_until_disconnected()


if __name__ == "__main__":
    with client:
        client.loop.run_until_complete(main())
