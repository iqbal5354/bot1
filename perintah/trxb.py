from telethon import events, Button

IS_USERBOT = True  # default

def init(client):
    global IS_USERBOT
    # kalau client jalan pakai bot token → bukan userbot
    if getattr(client, "_bot", False):
        IS_USERBOT = False
    else:
        IS_USERBOT = True

    # 📌 command utama
    @client.on(events.NewMessage(pattern=r"^\.trxb$"))
    async def trx_menu(event):
        if IS_USERBOT:
            # Userbot pakai Button.text
            buttons = [
                [Button.text("📋 Isi", resize=True)],
                [Button.text("💰 Dana Masuk", resize=True)],
            ]
            await event.respond("📖 **Menu TRX (Userbot)**", buttons=buttons)

        else:
            # Bot pakai Button.inline
            buttons = [
                [Button.inline("📋 Isi", b"isi")],
                [Button.inline("💰 Dana Masuk", b"dana")],
            ]
            await event.respond("📖 **Menu TRX (Bot)**", buttons=buttons)

    # 📌 handler Userbot (balasan text)
    @client.on(events.NewMessage(pattern="📋 Isi"))
    async def trx_isi(event):
        if IS_USERBOT:
            await event.reply("👉 Template Rekening:\nNama Bank:\nAtas Nama:\nNo Rek:")

    @client.on(events.NewMessage(pattern="💰 Dana Masuk"))
    async def trx_dana(event):
        if IS_USERBOT:
            await event.reply("👉 Dana masuk, lanjut serah terima data.")

    # 📌 handler Bot (inline callback)
    @client.on(events.CallbackQuery)
    async def callback_handler(event):
        if not IS_USERBOT:
            if event.data == b"isi":
                await event.edit("👉 Template Rekening:\nNama Bank:\nAtas Nama:\nNo Rek:")
            elif event.data == b"dana":
                await event.edit("👉 Dana masuk, lanjut serah terima data.")
