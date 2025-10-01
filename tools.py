# tools.py
from telethon import TelegramClient

# 🔹 Ambil OWNER_ID otomatis dari session / bot
async def get_owner_id(client: TelegramClient):
    me = await client.get_me()
    return me.id, me.username or me.first_name


# 🔹 Cek mode (userbot / bot)
def check_mode(client: TelegramClient):
    try:
        # ✅ Cara paling aman: cek apakah id diawali minus (bot) atau tidak (user)
        # Bot ID selalu berupa angka positif besar + diakhiri dengan 'bot' pada username
        if getattr(client, "_bot", False):
            return "BOT"

        if hasattr(client, "session"):
            session_name = str(client.session)
            if session_name.startswith("bot_session"):
                return "BOT"

        return "USERBOT"
    except Exception:
        return "USERBOT"
