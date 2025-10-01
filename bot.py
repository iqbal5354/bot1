import os
import sys
import asyncio
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.functions.channels import CreateChannelRequest
from telethon.tl.functions.messages import CreateChatRequest, ExportChatInviteRequest
from telethon.errors import FloodWaitError

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
SESSION = os.getenv("SESSION")

client = TelegramClient(StringSession(SESSION), API_ID, API_HASH)

OWNER_ID = None


async def init_owner():
    global OWNER_ID
    me = await client.get_me()
    OWNER_ID = me.id
    print(f"ℹ️ OWNER_ID otomatis diset ke: {OWNER_ID} ({me.username or me.first_name})")
    try:
        await client.send_message(OWNER_ID, "✅ Bot berhasil dijalankan dan siap dipakai.")
    except Exception:
        pass


# 🔹 Pesan template otomatis
pesan1 = """FORMAT TRANSAKSI

┏━━━━━━━━━━━━━━━━
┣ Jual Beli Apa  : 
┣ Penjual Siapa  : 
┣ Pembeli Siapa  :
┣ Harga Berapa   :
┗━━━━━━━━━━━━━━━━ 
PENTING!!!
☑️ Harap pasikan Transaksi tidak ada miskom buyer dan seller. 
☑️ Jika Transaksi Cancel Fee tetap Terpotong, jika tdk mau Terpotong Silahkan cari penjual lain.
☑️ Jadikan Saya Sebagai admin grub ini
✅ Janggn ganti judul MC."""

pesan2 = pesan1
pesan3 = """:: Uang sudah masuk di saya. Silahkan kalian serah terima data ::

━━━━PENTING!!━━━━
⚠️Harap Tanyakan dulu masalah Garansi.
⚠️Jgn coba2 ada drama jika tidak mau saya mintain ident via VC. Karena drama=ripper.
⚠️Jangan Berikan Hal2 yg rawan seperti OTP tele WA OTP email di luar transaksi
⚠️jika Pembeli tidak ada kabar selama 8 jam maka dana akan di cairkan dan jika penjual tidak ada kabar selama 5 jam uang di transfer balik ke pembeli
━━━━━━━━━━━━━"""


# 🔹 Fungsi bikin progress bar
def progress_bar(current, total, length=20):
    filled = int(length * current // total)
    bar = "█" * filled + "▒" * (length - filled)
    return f"[{bar}] {current}/{total}"


# 🔹 Command .id → cek ID grup/channel
@client.on(events.NewMessage(pattern=r"^\.id$"))
async def handler_id(event):
    chat = await event.get_chat()
    await event.delete()

    chat_id = chat.id
    if not str(chat_id).startswith("-100") and (event.is_group or event.is_channel):
        chat_id = f"-100{abs(chat_id)}"

    msg = await event.respond("🔍 Mencari ID chat...")
    await msg.edit(f"🆔 Chat ID: `{chat_id}`")


# 🔹 Command .buat → buat grup/channel dengan progress bar
@client.on(events.NewMessage(pattern=r"^\.buat (b|g|c) (\d+) (.+)"))
async def handler_buat(event):
    if event.sender_id != OWNER_ID:
        return

    jenis = event.pattern_match.group(1)
    jumlah = int(event.pattern_match.group(2))
    nama = event.pattern_match.group(3)

    await event.delete()
    msg = await event.respond("⏳ Sedang membuat group/channel...")

    try:
        hasil = []
        for i in range(1, jumlah + 1):
            nama_group = f"{nama} {i}" if jumlah > 1 else nama

            if jenis == "b":  # Buat basic group
                r = await client(CreateChatRequest(
                    users=[await client.get_me()],
                    title=nama_group,
                ))
                chat_id = r.chats[0].id
            else:  # Buat supergroup / channel
                r = await client(CreateChannelRequest(
                    title=nama_group,
                    about="GRUB BY @WARUNGBULLOVE",
                    megagroup=(jenis == "g"),
                ))
                chat_id = r.chats[0].id

            link = (await client(ExportChatInviteRequest(chat_id))).link

            if jenis == "g":
                await client.send_message(chat_id, "👋 Hallo, grup berhasil dibuat!")
                await client.send_message(chat_id, pesan1)
                await client.send_message(chat_id, pesan2)
                await client.send_message(chat_id, pesan3)

            hasil.append(f"✅ [{nama_group}]({link})")

            # update progress bar
            bar = progress_bar(i, jumlah)
            await msg.edit(f"🔄 Membuat group/channel...\n{bar}")

        # selesai → tampilkan hasil
        await msg.edit("🎉 Grup/Channel berhasil dibuat:\n\n" + "\n".join(hasil), link_preview=False)

    except FloodWaitError as e:
        await msg.edit(
            f"⚠️ Kena limit Telegram!\n"
            f"Tunggu {e.seconds//3600} jam {e.seconds%3600//60} menit ({e.seconds} detik)."
        )
    except Exception as e:
        await msg.edit(f"❌ Error: {str(e)}")


# 🔹 Command .restart
@client.on(events.NewMessage(pattern=r"^\.restart$"))
async def handler_restart(event):
    if event.sender_id != OWNER_ID:
        return
    await event.delete()
    await event.respond("♻️ Bot sedang restart...")
    args = [sys.executable] + sys.argv
    os.execv(sys.executable, args)


# === MAIN ===
async def main():
    print("🤖 Bot starting...")
    await init_owner()
    await client.run_until_disconnected()


if __name__ == "__main__":
    with client:
        client.loop.run_until_complete(main())
