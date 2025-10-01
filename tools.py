from telethon import TelegramClient

# 🔹 Ambil OWNER_ID otomatis dari session / bot
async def get_owner_id(client: TelegramClient):
    try:
        me = await client.get_me()
        return me.id, me.username or me.first_name
    except Exception as e:
        return None, f"Error: {e}"


# 🔹 Cek mode (userbot / bot)
def check_mode(client: TelegramClient):
    """
    Return "BOT" kalau pakai bot_token,
    otherwise "USERBOT".
    """
    if getattr(client, "_bot", False):
        return "BOT"
    return "USERBOT"
