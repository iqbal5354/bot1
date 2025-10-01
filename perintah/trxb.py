from telethon import events, Button

IS_USERBOT = True  # default, nanti bisa auto cek

def init(client):
    global IS_USERBOT
    # cek apakah client pakai bot token
    if client._bot:  
        IS_USERBOT = False
    else:
        IS_USERBOT = True

    # 📌 command utama
    @client.on(events.NewMessage(pattern=r"^\.trxb$"))
    async def trx_menu(event):
        if IS_USERBOT:
            # versi userbot → Button.text
            buttons = [
                [Button.text("📋 Isi", resize=True, single_use=True)],
                [Button.text("💰 Dana Masuk", resize=True, single_use=True)],
                [Button.text("📝 Format", resize=True, single_use=True)],
                [Button.text("📜 Aturan", resize=True, single_use=True)],
            ]
            await event.respond("📖 **Menu TRX**\nPilih salah satu tombol:", buttons=buttons)

        else:
            # versi bot → Button.inline
            buttons = [
                [Button.inline("📋 Isi", b"isi")],
                [Button.inline("💰 Dana Masuk", b"dana")],
                [Button.inline("📝 Format", b"format")],
                [Button.inline("📜 Aturan", b"aturan")],
            ]
            await event.respond("📖 **Menu TRX**\nPilih salah satu tombol:", buttons=buttons)

    # 📌 handler untuk userbot (text)
    @client.on(events.NewMessage(pattern="📋 Isi"))
    async def trx_isi(event):
        if IS_USERBOT:
            await event.reply("👉 **Template Rekening:**\n```\nNama Bank:\nAtas Nama:\nNo Rek:\n```")

    @client.on(events.NewMessage(pattern="💰 Dana Masuk"))
    async def trx_dana(event):
        if IS_USERBOT:
            await event.reply("👉 **Dana masuk! Silakan lanjut serah terima data.**")

    @client.on(events.NewMessage(pattern="📝 Format"))
    async def trx_format(event):
        if IS_USERBOT:
            await event.reply("👉 **Format TRX:**\n```\nTransaksi:\nPenjual:\nPembeli:\nHarga:\nFee:\n```")

    @client.on(events.NewMessage(pattern="📜 Aturan"))
    async def trx_aturan(event):
        if IS_USERBOT:
            await event.reply("👉 **Aturan Rekber:**\n1. Jangan kasih OTP.\n2. Jangan hilang saat transaksi.\n3. Cancel tetap kena fee.")

    # 📌 handler untuk bot (inline)
    @client.on(events.CallbackQuery)
    async def callback_handler(event):
        if not IS_USERBOT:
            if event.data == b"isi":
                await event.edit("👉 **Template Rekening:**\n```\nNama Bank:\nAtas Nama:\nNo Rek:\n```")
            elif event.data == b"dana":
                await event.edit("👉 **Dana masuk! Silakan lanjut serah terima data.**")
            elif event.data == b"format":
                await event.edit("👉 **Format TRX:**\n```\nTransaksi:\nPenjual:\nPembeli:\nHarga:\nFee:\n```")
            elif event.data == b"aturan":
                await event.edit("👉 **Aturan Rekber:**\n1. Jangan kasih OTP.\n2. Jangan hilang saat transaksi.\n3. Cancel tetap kena fee.")
