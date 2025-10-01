from telethon import events, Button

def init(client):
    @client.on(events.NewMessage(pattern=r"^\.trxb$"))
    async def trx_menu(event):
        buttons = [
            [Button.text("📋 Isi", resize=True)],
            [Button.text("💰 Dana Masuk", resize=True)],
            [Button.text("📝 Format", resize=True)],
            [Button.text("📜 Aturan", resize=True)],
        ]
        await event.respond("📖 **Menu TRX**\nPilih salah satu tombol:", buttons=buttons)
