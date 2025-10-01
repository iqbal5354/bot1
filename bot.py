import os
import importlib
from telethon import TelegramClient
from telethon.sessions import StringSession
from perintah.addbot import load_token  # ambil fungsi load_token

# Ambil ENV
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
SESSION = os.getenv("SESSION")

# Cek apakah ada token bot dari .addbot
BOT_TOKEN = load_token()

if BOT_TOKEN:
    print("🤖 Bullove BOT starting...")
    client = TelegramClient("bot_session", API_ID, API_HASH).start(bot_token=BOT_TOKEN)
else:
    print("🤖 Bullove Userbot starting...")
    client = TelegramClient(StringSession(SESSION), API_ID, API_HASH)


async def main():
    from tools import get_owner_id
    owner_id, owner_name = await get_owner_id(client)
    print(f"ℹ️ OWNER_ID otomatis diset ke: {owner_id} ({owner_name})")

    # Auto load semua file di folder "perintah"
    for file in os.listdir("perintah"):
        if file.endswith(".py") and not file.startswith("__"):
            modulename = file[:-3]
            module = importlib.import_module(f"perintah.{modulename}")
            if hasattr(module, "init"):
                module.init(client)
            if hasattr(module, "init_owner"):
                await module.init_owner(client)

    # Jalankan client
    await client.run_until_disconnected()


if __name__ == "__main__":
    with client:
        client.loop.run_until_complete(main())
