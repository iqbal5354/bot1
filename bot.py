import os
import sys
import asyncio
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.functions.channels import CreateChannelRequest
from telethon.tl.functions.messages import CreateChatRequest, ExportChatInviteRequest

# ==========================================================
# 🔹 Load ENV (API credentials wajib diset)
# ==========================================================
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
SESSION = os.getenv("SESSION")

# NOTE: OWNER_ID boleh tetap diset di ENV (opsional).
OWNER_ID = os.getenv("OWNER_ID")
OWNER_ID = int(OWNER_ID) if OWNER_ID and OWNER_ID.isdigit() else None

# ==========================================================
# 🔹 Init Client
# ==========================================================
client = TelegramClient(StringSession(SESSION), API_ID, API_HASH)

# ==========================================================
# 🔹 Pesan Template (sama seperti sebelumnya)
# ==========================================================
PESAN1 = """FORMAT TRANSAKSI

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
✅ Jangan ganti judul MC."""
PESAN2 = PESAN1
PESAN3 = """:: Uang sudah masuk di saya. Silahkan kalian serah terima data ::

━━━━PENTING!!━━━━
⚠️ Harap tanyakan dulu masalah Garansi.
⚠️ Jangan coba-coba ada drama jika tidak mau saya mintain ident via VC. Karena drama = ripper.
⚠️ Jangan berikan hal-hal yang rawan seperti OTP Telegram, WA, atau Email di luar transaksi.
⚠️ Jika pembeli tidak ada kabar selama 8 jam maka dana akan dicairkan. 
⚠️ Jika penjual tidak ada kabar selama 5 jam uang ditransfer balik ke pembeli.
━━━━━━━━━━━━━"""

# ==========================================================
# 🔹 Helper: kirim notifikasi ke owner (dipanggil setelah OWNER_ID dipastikan)
# ==========================================================
async def notify_owner():
    if OWNER_ID:
        try:
            await client.send_message(OWNER_ID, "✅ Bot berhasil dijalankan dan siap dipakai.")
        except Exception:
            # ignore jika gagal (mis. tidak bisa kirim)
            pass

# ==========================================================
# 🔹 Command: .id → cek Chat ID
# ==========================================================
@client.on(events.NewMessage(pattern=r"\.id"))
async def handler_id(event):
    chat = await event.get_chat()
    await event.delete()

    chat_id = chat.id
    if not str(chat_id).startswith("-100") and (event.is_group or event.is_channel):
        chat_id = f"-100{abs(chat_id)}"

    msg = await event.respond("🔍 Mencari ID chat...")
    await msg.edit(f"🆔 Chat ID: `{chat_id}`")


# ==========================================================
# 🔹 Command: .buatt (b/g/c) jumlah nama
# ==========================================================
@client.on(events.NewMessage(pattern=r"\.buatt (b|g|c) (\d+) (.+)"))
async def handler_buatt(event):
    jenis = event.pattern_match.group(1)
    jumlah = int(event.pattern_match.group(2))
    nama = event.pattern_match.group(3)

    await event.delete()
    msg = await event.respond("⏳ Mohon tunggu sebentar, sedang membuat group/channel...")

    try:
        hasil = []
        for i in range(1, jumlah + 1):
            nama_group = f"{nama} {i}" if jumlah > 1 else nama

            if jenis == "b":  # Basic Group
                r = await client(CreateChatRequest(users=[await client.get_me()], title=nama_group))
                chat_id = r.chats[0].id
                link = (await client(ExportChatInviteRequest(chat_id))).link
            else:  # Supergroup / Channel
                r = await client(CreateChannelRequest(
                    title=nama_group,
                    about="GRUB BY @WARUNGBULLOVE",
                    megagroup=(jenis == "g"),
                ))
                chat_id = r.chats[0].id
                link = (await client(ExportChatInviteRequest(chat_id))).link

            hasil.append(f"✅ [{nama_group}]({link})")

        await msg.edit("🎉 Grup/Channel berhasil dibuat:\n\n" + "\n".join(hasil), link_preview=False)

    except Exception as e:
        await msg.edit(f"❌ Error: {str(e)}")


# ==========================================================
# 🔹 Command: .buat g jumlah nama → hanya owner boleh (owner diset otomatis jika belum ada)
# ==========================================================
@client.on(events.NewMessage(pattern=r"\.buat g (\d+) (.+)"))
async def handler_buat(event):
    # global OWNER_ID  # tidak perlu declare di sini karena hanya membaca
    if OWNER_ID and event.sender_id != OWNER_ID:
        return

    await event.delete()
    jumlah = int(event.pattern_match.group(1))
    nama = event.pattern_match.group(2)

    msg = await event.respond("⏳ Mohon tunggu sebentar, sedang membuat grup...")

    hasil = []
    for i in range(jumlah):
        grup = await client(CreateChannelRequest(
            title=f"{nama} {i+1}",
            about="GRUB BY @WARUNGBULLOVE",
            megagroup=True
        ))
        chat_id = grup.chats[0].id

        # Kirim pesan otomatis
        await client.send_message(chat_id, "👋 Hallo, grup berhasil dibuat!")
        await client.send_message(chat_id, PESAN1)
        await client.send_message(chat_id, PESAN2)
        await client.send_message(chat_id, PESAN3)

        hasil.append(f"{i+1}. Grup **{nama} {i+1}** → `{chat_id}`")

    await msg.edit("✅ Grup berhasil dibuat:\n\n" + "\n".join(hasil))


# ==========================================================
# 🔹 Command: .restart → restart bot
# ==========================================================
@client.on(events.NewMessage(pattern=r"\.restart"))
async def handler_restart(event):
    await event.delete()
    await event.respond("♻️ Bot sedang restart...")

    args = [sys.executable] + sys.argv
    os.execv(sys.executable, args)


# ==========================================================
# 🔹 Main: set OWNER_ID otomatis jika belum diset di ENV
# ==========================================================
async def main():
    global OWNER_ID
    print("🤖 Bot starting...")

    # pastikan client sudah terhubung dan session valid
    await client.connect()
    if not await client.is_user_authorized():
        # Jika session belum authorized, stop dengan jelas
        print("❌ Session tidak ter-autentikasi. Pastikan SESSION String benar.")
        await client.disconnect()
        return

    # Jika OWNER_ID belum diset via ENV, ambil dari akun saat ini (deployer)
    if OWNER_ID is None:
        me = await client.get_me()
        OWNER_ID = me.id
        print(f"ℹ️ OWNER_ID otomatis diset ke: {OWNER_ID} ({getattr(me, 'username', 'no-username')})")

    # Kirim notif ke owner (opsional)
    await notify_owner()

    # Jalankan loop event sampai disconnected
    await client.run_until_disconnected()


if __name__ == "__main__":
    with client:
        client.loop.run_until_complete(main())
