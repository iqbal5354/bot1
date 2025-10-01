# perintah/__init__.py

def hello():
    return "📂 Folder perintah siap dipakai."
from .commands import register_commands, init_owner
from .trx import register_trx
from .ai import register_ai, init_owner_ai
from .speedtest import register_speedtest, init_owner_speed

async def init_all_owner(client):
    await init_owner(client)
    await init_owner_ai(client)
    await init_owner_speed(client)

def init(client):
    register_commands(client)
    register_trx(client)
    register_ai(client)
    register_speedtest(client)
