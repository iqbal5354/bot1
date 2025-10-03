from telethon import events
from datetime import datetime
import asyncio

OWNER_ID = 123456789  # ganti dengan ID kamu

@client.on(events.NewMessage(pattern=r"^\.gas$"))
async def handler_gas(event):
    if event.sender_id != OWNER_ID:
        return

    try:
        async with client.conversation(event.chat_id, timeout=5) as conv:
            # 1. pilih jenis
            await conv.send_message("Mau grub atau channel? (ketik g/c)")
            jenis = (await conv.get_response()).raw_text.strip().lower()

            # 2. jumlah
            await conv.send_message("Jumlah yang akan dibuat berapa?")
            jumlah = int((await conv.get_response()).raw_text.strip())

            # 3. nama
            await conv.send_message("Nama grub apa?")
            nama = (await conv.get_response()).raw_text.strip()

            # 4. pesan otomatis?
            await conv.send_message("Apakah ingin mengirim pesan otomatis ke grup/channel? (Y/N)")
            auto = (await conv.get_response()).raw_text.strip().lower()

            pesan_jumlah = 0
            if auto == "y":
                await conv.send_message("Berapa pesan otomatis yang ingin dikirim?")
                pesan_jumlah = int((await conv.get_response()).raw_text.strip())

    except asyncio.TimeoutError:
        await event.respond("⏰ Waktu habis! Kamu tidak menjawab dalam 5 detik.")
        return

    # mulai eksekusi bikin grup/channel
    berhasil = 0
    gagal = 0

    for i in range(jumlah):
        try:
            if jenis == "g":  # bikin grup
                result = await client(functions.messages.CreateChatRequest(
                    users=[event.sender_id],
                    title=f"{nama} {i+1}"
                ))
            elif jenis == "c":  # bikin channel
                result = await client(functions.channels.CreateChannelRequest(
                    title=f"{nama} {i+1}",
                    about="Channel otomatis",
                    megagroup=False
                ))
            else:
                await event.respond("❌ Jenis tidak valid, hanya bisa g/c.")
                return

            berhasil += 1

            # kalau ada pesan otomatis
            if auto == "y" and pesan_jumlah > 0:
                for x in range(pesan_jumlah):
                    await client.send_message(result.chats[0].id, f"Pesan otomatis ke-{x+1}")

        except Exception:
            gagal += 1

    # ambil detail waktu
    now = datetime.now()
    hari = now.strftime("%A")
    jam = now.strftime("%H:%M:%S")
    tanggal = now.strftime("%d %B %Y")

    # hasil akhir
    if gagal == 0:
        detail = f"""
🕒 Detail:
- jumlah berhasil di buat : {berhasil}
- jumlah gagal di buat : {gagal}

- Hari   : {hari}
- Jam    : {jam}
- Tanggal: {tanggal}
"""
    else:
        detail = f"""
🕒 Detail:
- jumlah berhasil di buat : {berhasil}

- Hari   : {hari}
- Jam    : {jam}
- Tanggal: {tanggal}
"""

    await event.respond(f"✅ Selesai!\n{detail}")
