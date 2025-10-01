import os
from telethon import events
from bot import save_token, load_token

TOKEN_FILE = "bot_token.txt"

def init(client):
    # Tambah Bot Token
    @client.on(events.NewMessage(pattern=r"^\.addbot(?:\s+(.+))?"))
    async def handler_addbot(event):
        token = event.pattern_match.group(1)

        if not token:
            await event.reply(
                "⚠️ Kamu harus memberikan token bot!\n\n"
                "Contoh:\n`.addbot 123456:ABC-YourTokenHere`\n\n"
                "👉 Buat token baru di @BotFather kalau belum punya."
            )
            return

        save_token(token.strip())
        await event.reply("✅ Bot token berhasil disimpan. Restart untuk beralih ke **BOT mode**.")

    # Hapus Bot Token
    @client.on(events.NewMessage(pattern=r"^\.delbot$"))
    async def handler_delbot(event):
        if os.path.exists(TOKEN_FILE):
            os.remove(TOKEN_FILE)
            await event.reply("🗑️ Token bot berhasil dihapus. Restart untuk kembali ke **Userbot mode**.")
        else:
            await event.reply("ℹ️ Tidak ada token bot yang tersimpan.")

    # Cek Bot Token
    @client.on(events.NewMessage(pattern=r"^\.checkbot$"))
    async def handler_checkbot(event):
        token = load_token()
        if token:
            await event.reply("🤖 Token bot sudah tersimpan.\n\n👉 Jalankan **restart** untuk aktifkan BOT mode.")
        else:
            await event.reply("❌ Belum ada token bot.\n\nTambahkan dengan perintah: `.addbot <token>`")
