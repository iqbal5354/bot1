# tools.py
from telethon import TelegramClient

# 🔹 Ambil OWNER_ID otomatis dari session / bot
async def get_owner_id(client: TelegramClient):
    me = await client.get_me()
    return me.id, me.username or me.first_name


# 🔹 Cek mode (userbot / bot)
def check_mode(client: TelegramClient):
    # client._bot = True kalau pakai bot_token
    if hasattr(client, "_bot") and client._bot:
        return "BOT"
    return "USERBOT"

