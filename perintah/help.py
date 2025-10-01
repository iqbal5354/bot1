import importlib
import os
from telethon import events

HELP = {}

def load_help():
    global HELP
    HELP.clear()

    for file in os.listdir("perintah"):
        if file.endswith(".py") and not file.startswith("__") and file != "help.py":
            modulename = file[:-3]
            module = importlib.import_module(f"perintah.{modulename}")
            if hasattr(module, "HELP"):
                for section, cmds in module.HELP.items():
                    HELP.setdefault(section, []).extend(cmds)


def register_help(client):
    @client.on(events.NewMessage(pattern=r"^\.help$"))
    async def handler_help(event):
        await event.delete()
        if not HELP:
            load_help()

        text = "🤖 **Daftar Perintah Bullove Userbot**\n\n"
        for section, cmds in HELP.items():
            text += f"📌 **{section.capitalize()}**\n"
            for cmd in cmds:
                text += f"   • {cmd}\n"
            text += "\n"

        await event.respond(text.strip(), link_preview=False)


def init(client):
    load_help()
    register_help(client)
