# tools.py
from telethon import TelegramClient

# 🔹 Ambil OWNER_ID otomatis dari session / bot
async def get_owner_id(client: TelegramClient):
    me = await client.get_me()
    return me.id, me.username or me.first_name


# 🔹 Cek mode (userbot / bot)
def check_mode(client: TelegramClient):
    try:
        # Kalau memang ada flag _bot
        if hasattr(client, "_bot") and client._bot:
            return "BOT"

        # Kalau session namanya 'bot_session' → berarti bot
        if hasattr(client, "session") and str(client.session).startswith("bot_session"):
            return "BOT"

        # Default → userbot
        return "USERBOT"
    except Exception:
        return "USERBOT"
