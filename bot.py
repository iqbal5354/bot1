import os
import sys
from telethon import TelegramClient
from telethon.sessions import StringSession

# Ambil ENV
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
SESSION = os.getenv("SESSION")

# Inisialisasi client
client = TelegramClient(StringSession(SESSION), API_ID, API_HASH)

# Import commands
import commands


async def main():
    print("🤖 Bot starting...")
    # inisialisasi OWNER_ID
    await commands.init_owner(client)
    # daftarkan semua perintah
    commands.init(client)
    # jalanin client
    await client.run_until_disconnected()


if __name__ == "__main__":
    with client:
        client.loop.run_until_complete(main())
