import os
import importlib
from telethon import TelegramClient
from telethon.sessions import StringSession

# Ambil ENV
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
SESSION = os.getenv("SESSION")

# Inisialisasi client
client = TelegramClient(StringSession(SESSION), API_ID, API_HASH)


async def main():
    print("🤖 Bullove Userbot starting...")

    # Auto load semua file di folder "perintah"
    for file in os.listdir("perintah"):
        if file.endswith(".py") and not file.startswith("__"):
            modulename = file[:-3]
            module = importlib.import_module(f"perintah.{modulename}")
            if hasattr(module, "init"):
                module.init(client)   # panggil init(client)
            if hasattr(module, "init_owner"):
                await module.init_owner(client)

    # Jalankan client
    await client.run_until_disconnected()


if __name__ == "__main__":
    with client:
        client.loop.run_until_complete(main())
