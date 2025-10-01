import sys
import os
import time
import asyncio
from telethon import events
from telethon.tl.functions.channels import CreateChannelRequest
from telethon.tl.functions.messages import CreateChatRequest, ExportChatInviteRequest
from telethon.errors import FloodWaitError

OWNER_ID = None

async def init_owner(client):
    global OWNER_ID
    me = await client.get_me()
    OWNER_ID = me.id
    print(f"ℹ️ OWNER_ID otomatis diset ke: {OWNER_ID} ({me.username or me.first_name})")
    try:
        await client.send_message(OWNER_ID, "✅ Bot berhasil dijalankan dan siap dipakai.")
    except Exception:
        pass


# 🔹 Progress bar helper
def progress_bar(current, total, length=20):
    filled = int(length * current // total)
    bar = "█" * filled + "▒" * (length - filled)
    return f"[{bar}] {current}/{total}"


# 🔹 Animasi loading helper
async def animate_loading(msg, text, delay=0.3):
    frames = ["⏳", "⌛", "🔄", "🌀", "⚙️"]
    for frame in frames:
        await msg.edit(f"{frame} {text}")
        await asyncio.sleep(delay)


# === COMMANDS ===
def register_commands(client):

    # 📌 .ping
    @client.on(events.NewMessage(pattern=r"^\.ping$"))
    async def handler_ping(event):
        start = time.perf_counter()
        await event.edit("🏓 Pong...")
        end = time.perf_counter()
        ping_ms = int((end - start) * 1000)
        await event.edit(f"🏓 Pong!\n⏱ {ping_ms} ms")

    # 📌 .help
    @client.on(events.NewMessage(pattern=r"^\.help$"))
    async def handler_help(event):
        help_text = """
🤖 **Daftar Perintah Bot**

📌 Utility:
- `.ping` → cek respon bot
- `.id` → cek ID grup/channel
- `.restart` → restart bot

📌 Grup & Channel:
- `.buat g <jumlah?> <nama>` → buat supergroup
- `.buat c <jumlah?> <nama>` → buat channel
- `.buat b <jumlah?> <nama>` → buat basic group
  (jumlah opsional, default 1)

📌 Contoh:
- `.buat g 1 Warung BulLove`
- `.buat c 2 Channel Promo`
- `.buat g Warung MC`  (otomatis 1 grup)
"""
        await event.edit(help_text)

    # 📌 .id
    @client.on(events.NewMessage(pattern=r"^\.id$"))
    async def handler_id(event):
        chat = await event.get_chat()
        chat_id = chat.id
        if not str(chat_id).startswith("-100") and (event.is_group or event.is_channel):
            chat_id = f"-100{abs(chat_id)}"
        await event.edit(f"🆔 Chat ID: {chat_id}")

    # 📌 .buat
    @client.on(events.NewMessage(pattern=r"^\.buat (b|g|c)(?: (\d+))? (.+)"))
    async def handler_buat(event):
        if event.sender_id != OWNER_ID:
            return

        jenis = event.pattern_match.group(1)
        jumlah = int(event.pattern_match.group(2)) if event.pattern_match.group(2) else 1
        nama = event.pattern_match.group(3)

        msg = await event.respond("⏳ Menyiapkan pembuatan group/channel...")

        try:
            hasil = []
            for i in range(1, jumlah + 1):
                nama_group = f"{nama} {i}" if jumlah > 1 else nama

                # 🔹 animasi loading tiap step
                await animate_loading(msg, f"Membuat {nama_group} ({i}/{jumlah})")

                if jenis == "b":
                    r = await client(CreateChatRequest(
                        users=[await client.get_me()],
                        title=nama_group,
                    ))
                    chat_id = r.chats[0].id
                else:
                    r = await client(CreateChannelRequest(
                        title=nama_group,
                        about="GRUB BY @WARUNGBULLOVE",
                        megagroup=(jenis == "g"),
                    ))
                    chat_id = r.chats[0].id

                link = (await client(ExportChatInviteRequest(chat_id))).link
                hasil.append(f"✅ [{nama_group}]({link})")

                bar = progress_bar(i, jumlah)
                await msg.edit(f"🔄 Membuat group/channel...\n{bar}")

            await msg.edit("🎉 Grup/Channel berhasil dibuat:\n\n" + "\n".join(hasil), link_preview=False)

        except FloodWaitError as e:
            await msg.edit(f"⚠️ Kena limit Telegram!\nTunggu {e.seconds//3600} jam {e.seconds%3600//60} menit.")
        except Exception as e:
            await msg.edit(f"❌ Error: {str(e)}")

    # 📌 .restart
    @client.on(events.NewMessage(pattern=r"^\.restart$"))
    async def handler_restart(event):
        if event.sender_id != OWNER_ID:
            return
        await event.edit("♻️ Bot sedang restart...")
        args = [sys.executable] + sys.argv
        os.execv(sys.executable, args)


# Panggil fungsi ini di bot.py setelah client dibuat
def init(client):
    register_commands(client)
