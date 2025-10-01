import os
from telethon import events

TOKEN_FILE = "bot_token.txt"

def save_token(token):
    with open(TOKEN_FILE, "w") as f:
        f.write(token.strip())

def load_token():
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "r") as f:
            return f.read().strip()
    return None

def del_token():
    if os.path.exists(TOKEN_FILE):
        os.remove(TOKEN_FILE)

def init(client):
    @client.on(events.NewMessage(pattern=r"^\.addbot(?:\s+(.*))?"))
    async def handler(event):
        token = event.pattern_match.group(1)
        if not token:
            await event.reply("⚠️ Tolong sertakan token bot.\nContoh: `.addbot <TOKEN>`")
            return

        save_token(token)
        await event.reply("✅ Token bot tersimpan.\n🔄 Silakan **restart bot** agar aktif.")

        os._exit(0)  # langsung matikan agar auto-restart di container

    @client.on(events.NewMessage(pattern=r"^\.checkbot$"))
    async def check(event):
        from bot import client
        token = load_token()
        if token:
            me = await client.get_me()
            await event.reply(f"🤖 Bot aktif: **{me.first_name}** (@{me.username})")
        else:
            await event.reply("❌ Tidak ada token bot tersimpan.")

    @client.on(events.NewMessage(pattern=r"^\.delbot$"))
    async def delete(event):
        del_token()
        await event.reply("🗑️ Token bot dihapus.\n🔄 Silakan restart untuk kembali ke mode userbot.")
        os._exit(0)
