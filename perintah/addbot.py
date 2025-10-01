from telethon import events
from bot import save_token  # ambil fungsi simpan token dari bot.py

def init(client):
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
