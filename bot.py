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

# Ambil ENV dari Railway
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")  # kalau pakai bot
SESSION = os.getenv("SESSION")      # kalau pakai userbot

# Tentukan mode
if BOT_TOKEN:
    logging.info("🤖 Bullove BOT starting...")
    client = TelegramClient("bot_session", API_ID, API_HASH).start(bot_token=BOT_TOKEN)
else:
    logging.info("🤖 Bullove Userbot starting...")
    client = TelegramClient(StringSession(SESSION), API_ID, API_HASH)


async def main():
    from tools import get_owner_id, check_mode

    # Cek identitas owner
    try:
        owner_id, owner_name = await get_owner_id(client)
        logging.info(f"ℹ️ OWNER_ID otomatis diset ke: {owner_id} ({owner_name})")
    except Exception as e:
        logging.error(f"❌ Gagal mendapatkan owner id: {e}", exc_info=True)

    # Cek mode
    mode = check_mode(client)
    logging.info(f"🔧 Mode berjalan: {mode}")

    # Auto load semua file di folder "perintah"
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
