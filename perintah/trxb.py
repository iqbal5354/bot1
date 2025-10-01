from telethon import events, Button

def init(client):
    @client.on(events.NewMessage(pattern=r"^\.trxb$"))
    async def trx_menu(event):
        buttons = [
            [Button.text("📋 Isi")],
            [Button.text("💰 Dana Masuk")],
            [Button.text("📝 Format")],
            [Button.text("📜 Aturan")],
        ]
        await event.reply("📖 **Menu TRX**\nPilih salah satu tombol:", buttons=buttons)
