import os
from telethon import events

TOKEN_FILE = "bottoken.txt"


# 🔹 Simpan token ke file + ENV
def save_token(token: str):
    with open(TOKEN_FILE, "w") as f:
        f.write(token.strip())
    os.environ["BOT_TOKEN"] = token.strip()


# 🔹 Ambil token dari ENV atau file
def load_token():
    token = os.getenv("BOT_TOKEN")
    if token:
        return token.strip()
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE) as f:
            return f.read().strip()
    return None


def init(client):
    @client.on(events.NewMessage(pattern=r"^\.addbot(?:\s+(.+))?$"))
    async def handler(event):
        token = event.pattern_match.group(1)

        if not token:
            await event.reply(
                "❌ Kamu harus memberikan token bot.\n\n"
                "**Contoh:** `.addbot 123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`"
            )
            return

        save_token(token)
        await event.reply(
            f"✅ Token bot berhasil disimpan!\n\n"
            "👉 Silakan **restart ulang** untuk menjalankan mode BOT."
        )
