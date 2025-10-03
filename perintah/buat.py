import asyncio
import random
import datetime
from telethon import events
from telethon.tl.functions.channels import CreateChannelRequest
from telethon.tl.functions.messages import CreateChatRequest, ExportChatInviteRequest
from telethon.errors import FloodWaitError

from .random_messages import RANDOM_MESSAGES  # import pesan otomatis

OWNER_ID = None

# === OWNER INIT ===
async def init_owner(client):
    global OWNER_ID
    me = await client.get_me()
    OWNER_ID = me.id

# === HELPERS ===
def format_detail(success, failed):
    now = datetime.datetime.now()
    hari = now.strftime("%A")
    jam = now.strftime("%H:%M:%S")
    tanggal = now.strftime("%d %B %Y")

    if failed > 0:
        return (
            f"\n🕒 Detail:\n"
            f"- jumlah berhasil di buat : {success}\n\n"
            f"- Hari   : {hari}\n"
            f"- Jam    : {jam}\n"
            f"- Tanggal: {tanggal}"
        )
    else:
        return (
            f"\n🕒 Detail:\n"
            f"- jumlah berhasil di buat : {success}\n"
            f"- jumlah gagal di buat : {failed}\n\n"
            f"- Hari   : {hari}\n"
            f"- Jam    : {jam}\n"
            f"- Tanggal: {tanggal}"
        )

# === COMMAND .buat ===
def init(client):

    @client.on(events.NewMessage(pattern=r"^\.gas$"))
    async def handler_buat(event):
        if event.sender_id != OWNER_ID:
            return

        # hapus command .buat
        await event.delete()

        chat = await event.get_chat()
        input_msgs = []  # simpan semua jawaban user untuk nanti dihapus

        # Step 1: Jenis grup atau channel
        tanya1 = await client.send_message(chat.id, "🚀 Pembuatan baru dimulai...\nMau **Grub** atau **Channel**?\nKetik `g` untuk grub / `c` untuk channel")
        response1 = await client.wait_for(events.NewMessage(from_users=OWNER_ID, chats=chat.id))
        jenis = response1.raw_text.strip().lower()
        input_msgs.append(response1.message)

        # Step 2: Jumlah
        tanya2 = await client.send_message(chat.id, "📌 Jumlah yang akan dibuat berapa?")
        response2 = await client.wait_for(events.NewMessage(from_users=OWNER_ID, chats=chat.id))
        jumlah = int(response2.raw_text.strip())
        input_msgs.append(response2.message)

        # Step 3: Nama
        tanya3 = await client.send_message(chat.id, "📌 Nama grup/channel apa?")
        response3 = await client.wait_for(events.NewMessage(from_users=OWNER_ID, chats=chat.id))
        nama = response3.raw_text.strip()
        input_msgs.append(response3.message)

        # Step 4: Pesan otomatis Y/N
        tanya4 = await client.send_message(chat.id, "❓ Apakah ingin ada pesan otomatis? (Y/N)")
        response4 = await client.wait_for(events.NewMessage(from_users=OWNER_ID, chats=chat.id))
        auto_pesan = response4.raw_text.strip().lower()
        input_msgs.append(response4.message)

        jumlah_pesan = 0
        if auto_pesan == "y":
            tanya5 = await client.send_message(chat.id, "✉️ Berapa jumlah pesan otomatis?")
            response5 = await client.wait_for(events.NewMessage(from_users=OWNER_ID, chats=chat.id))
            jumlah_pesan = int(response5.raw_text.strip())
            input_msgs.append(response5.message)

        hasil = []
        sukses, gagal = 0, 0

        status_msg = await client.send_message(chat.id, "⏳ Membuat grup/channel...")

        for i in range(1, jumlah + 1):
            nama_group = f"{nama} {i}" if jumlah > 1 else nama
            try:
                if jenis == "g":
                    r = await client(CreateChatRequest(
                        users=[await client.get_me()],
                        title=nama_group,
                    ))
                    chat_id = r.chats[0].id
                else:
                    r = await client(CreateChannelRequest(
                        title=nama_group,
                        about="Dibuat otomatis oleh bot",
                        megagroup=(jenis == "g"),
                    ))
                    chat_id = r.chats[0].id

                link = (await client(ExportChatInviteRequest(chat_id))).link
                hasil.append(f"✅ [{nama_group}]({link})")
                sukses += 1

                # kirim pesan otomatis
                if jumlah_pesan > 0:
                    for _ in range(jumlah_pesan):
                        pesan = random.choice(RANDOM_MESSAGES)
                        try:
                            await client.send_message(chat_id, pesan)
                            await asyncio.sleep(1)
                        except FloodWaitError as fw:
                            await asyncio.sleep(fw.seconds)
                            await client.send_message(chat_id, pesan)

            except Exception as e:
                hasil.append(f"⚠️ {nama_group} gagal dibuat ({str(e)})")
                gagal += 1

        # hapus semua jawaban input user
        for m in input_msgs:
            try:
                await m.delete()
            except:
                pass

        # edit status jadi hasil akhir
        await status_msg.edit("🎉 Hasil Pembuatan:\n\n" + "\n".join(hasil) + format_detail(sukses, gagal), link_preview=False)
