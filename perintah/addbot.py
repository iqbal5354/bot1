import json
from telethon import events

CONFIG_FILE = "config.json"

def save_token(token: str):
    with open(CONFIG_FILE, "w") as f:
        json.dump({"BOT_TOKEN": token}, f)

def load_token():
    try:
        with open(CONFIG_FILE, "r") as f:
            data = json.load(f)
            return data.get("BOT_TOKEN")
    except FileNotFoundError:
        return None


def init(client):
    @client.on(events.NewMessage(pattern=r"^\.addbot (.+)$"))
    async def add_bot(event):
        token = event.pattern_match.group(1)
        save_token(token)
        await event.reply("✅ BOT_TOKEN berhasil disimpan. Restart bot untuk mengaktifkan mode Bot.")
