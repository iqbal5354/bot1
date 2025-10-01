import os
import sys
from telethon import TelegramClient
from perintah import init_all_owner, init   # ambil semua modul di folder perintah

# ===== Konfigurasi API (gunakan variabel ENV agar aman) =====
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
SESSION = os.getenv("SESSION", "userbot")  # default session = "userbot"

# Inisialisasi client
client = TelegramClient(SESSION, API_ID, API_HASH)


async def main():
    print("🤖 Bot sedang start...")

    # 🔹 Set OWNER_ID otomatis dari akun yg login
    await init_all_owner(client)

    # 🔹 Daftarkan semua perintah dari folder perintah
    init(client)

    print("✅ Bot sudah jalan. Tekan Ctrl+C untuk stop.")
    await client.run_until_disconnected()


if __name__ == "__main__":
    with client:
        client.loop.run_until_complete(main())
