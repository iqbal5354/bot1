import sys
import time
from telethon import events

OWNER_ID = None

async def init_owner(client):
    global OWNER_ID
    me = await client.get_me()
    OWNER_ID = me.id
    print(f"ℹ️ OWNER_ID otomatis diset ke: {OWNER_ID} ({me.username or me.first_name})")

    try:
        await client.send_message(OWNER_ID, "✅ Bot berhasil dijalankan dan siap dipakai.")
    except:
        pass


def init(client):
    # 📌 .ping
    @client.on(events.NewMessage(pattern=r"^\.ping$"))
    async def handler_ping(event):
        start = time.perf_counter()
        msg = await event.respond("🏓 Pong...")
        end = time.perf_counter()
        ping_ms = int((end - start) * 1000)
        await msg.edit(f"🏓 Pong!\n⏱ {ping_ms} ms")

    # 📌 .help
    @client.on(events.NewMessage(pattern=r"^\.help$"))
    async def handler_help(event):
        help_text = """
🤖 **Daftar Perintah Bot**

📌 Utility:
- `.ping` → cek respon bot
- `.id` → cek ID grup/channel
- `.restart` → restart bot
"""
        await event.respond(help_text)
