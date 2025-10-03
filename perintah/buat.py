import asyncio
import random
import datetime
import logging
from telethon import events
from telethon.tl.functions.channels import CreateChannelRequest
from telethon.tl.functions.messages import CreateChatRequest, ExportChatInviteRequest
from telethon.errors import FloodWaitError

from .random_messages import RANDOM_MESSAGES

OWNER_ID = None

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

async def init_owner(client):
    global OWNER_ID
    me = await client.get_me()
    OWNER_ID = me.id
    logging.info(f"OWNER_ID di-set ke {OWNER_ID}")

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

def init(client):

    @client.on(events.NewMessage(pattern=r"^\.gas$"))
    async def handler_gas(event):
        if event.sender_id != OWNER_ID:
            return

        chat = await event.get_chat()
        hasil = []
        sukses, gagal = 0, 0

        try:
            async with client.conversation(chat.id, exclusive=True) as conv:
                # Step 1: pilih jenis
                await conv.send_message(
                    "🚀 Pembuatan baru dimulai...\n"
                    "Mau **Grub** atau **Channel**?\n"
                    "Ketik `g` untuk grub / `c` untuk channel"
                )
                resp = await conv.wait_event(events.NewMessage(from_users=event.sender_id), timeout=30)
                jenis = resp.raw_text.strip().lower()
                logging.info(f"Jenis dipilih: {jenis}")

                # Step 2: jumlah
                await conv.send_message("📌 Jumlah yang akan dibuat berapa?")
                resp = await conv.wait_event(events.NewMessage(from_users=event.sender_id), timeout=30)
                jumlah = int(resp.raw_text.strip())
                logging.info(f"Jumlah yang diminta: {jumlah}")

                # Step 3: nama
                await conv.send_message("📌 Nama grup/channel apa?")
                resp = await conv.wait_event(events.NewMessage(from_users=event.sender_id), timeout=30)
                nama = resp.raw_text.strip()
                logging.info(f"Nama yang diminta: {nama}")

                # Step 4: pesan otomatis
                await conv.send_message("❓ Apakah ingin ada pesan otomatis? (Y/N)")
                resp = await conv.wait_event(events.NewMessage(from_users=event.sender_id), timeout=30)
                auto_pesan = resp.raw_text.strip().lower()
                logging.info(f"Pesan otomatis dipilih: {auto_pesan}")

                jumlah_pesan = 0
                if auto_pesan == "y":
                    await conv.send_message("✉️ Berapa jumlah pesan otomatis?")
                    resp = await conv.wait_event(events.NewMessage(from_users=event.sender_id), timeout=30)
                    jumlah_pesan = int(resp.raw_text.strip())
                    logging.info(f"Jumlah pesan otomatis: {jumlah_pesan}")

        except asyncio.TimeoutError:
            await client.send_message(chat.id, "❌ Gagal dijalankan karena waktu habis.")
            logging.error("Timeout: Tidak ada respon dari user")
            return

        # Status sementara
        status_msg = await client.send_message(chat.id, "⏳ Membuat grup/channel...")

        # Buat grup/channel
        for i in range(1, jumlah + 1):
            nama_group = f"{nama} {i}" if jumlah > 1 else nama
            try:
                if jenis == "g":
                    r = await client(CreateChatRequest(
                        users=[await client.get_me()],
                        title=nama_group,
                    ))
                    # FIX: CreateChatRequest return InvitedUsers, ambil chat_id dengan cara ini
                    chat_id = r.chats[0].id
                    logging.info(f"Grup berhasil dibuat: {nama_group} (id={chat_id})")

                else:
                    r = await client(CreateChannelRequest(
                        title=nama_group,
                        about="Dibuat otomatis oleh bot",
                        megagroup=(jenis == "g"),
                    ))
                    chat_id = r.chats[0].id
                    logging.info(f"Channel berhasil dibuat: {nama_group} (id={chat_id})")

                link = (await client(ExportChatInviteRequest(chat_id))).link
                hasil.append(f"✅ [{nama_group}]({link})")
                sukses += 1

                # Pesan otomatis
                if jumlah_pesan > 0:
                    for _ in range(jumlah_pesan):
                        pesan = random.choice(RANDOM_MESSAGES)
                        try:
                            await client.send_message(chat_id, pesan)
                            await asyncio.sleep(1)
                            logging.info(f"Pesan otomatis terkirim ke {nama_group}")
                        except FloodWaitError as fw:
                            logging.warning(f"FloodWait {fw.seconds} detik, menunggu...")
                            await asyncio.sleep(fw.seconds)
                            await client.send_message(chat_id, pesan)

            except Exception as e:
                hasil.append(f"⚠️ {nama_group} gagal dibuat ({str(e)})")
                gagal += 1
                logging.error(f"Gagal membuat {nama_group}: {str(e)}")

        # Edit status ke hasil akhir
        await status_msg.edit(
            "🎉 Hasil Pembuatan:\n\n" + "\n".join(hasil) + format_detail(sukses, gagal),
            link_preview=False,
        )
