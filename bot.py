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
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
SESSION = os.getenv("SESSION", None)
BOT_TOKEN = os.getenv("BOT_TOKEN", None)  # langsung dari Railway Variables
MODE = os.getenv("MODE", "BOT").upper()   # pilih BOT / USERBOT

# Tentukan client sesuai mode
if MODE == "BOT" and BOT_TOKEN:
    logging.info("🤖 Bullove BOT starting...")

    # Gunakan session file agar tidak login ulang tiap restart
    client = TelegramClient("bot_session", API_ID, API_HASH)

    try:
        client.start(bot_token=BOT_TOKEN)  # login pertama kali
    except Exception as e:
        logging.error(f"❌ Gagal start bot: {e}", exc_info=True)

elif MODE == "USERBOT" and SESSION:
    logging.info("🤖 Bullove USERBOT starting...")
    client = TelegramClient(StringSession(SESSION), API_ID, API_HASH)

else:
    raise SystemExit("❌ Tidak ada konfigurasi yang valid! Set MODE=BOT + BOT_TOKEN atau MODE=USERBOT + SESSION")


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
