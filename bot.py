import os
import importlib
from telethon import TelegramClient
from telethon.sessions import StringSession

# === Fungsi simpan & ambil token Bot ===
TOKEN_FILE = "bot_token.txt"

def save_token(token: str):
    with open(TOKEN_FILE, "w") as f:
        f.write(token.strip())

def load_token() -> str | None:
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "r") as f:
            return f.read().strip()
    return None

# === Ambil ENV untuk Userbot ===
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
SESSION = os.getenv("SESSION")

# === Pilih mode Bot atau Userbot ===
BOT_TOKEN = load_token()
if BOT_TOKEN:
    print("🤖 Bullove BOT starting...")
    client = TelegramClient("bot_session", API_ID, API_HASH).start(bot_token=BOT_TOKEN)
else:
    print("🤖 Bullove Userbot starting...")
    client = TelegramClient(StringSession(SESSION), API_ID, API_HASH)


# === Main ===
async def main():
    # Auto load semua file di folder "perintah"
    for file in os.listdir("perintah"):
        if file.endswith(".py") and not file.startswith(""):
            modulename = file[:-3]
            module = importlib.import_module(f"perintah.{modulename}")
            if hasattr(module, "init"):
                module.init(client)   # panggil init(client)
            if hasattr(module, "init_owner"):
                await module.init_owner(client)

    # Jalankan client
    await client.run_until_disconnected()


if __name == "main":
    with client:
        client.loop.run_until_complete(main())
