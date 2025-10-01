from .commands import register_commands, init_owner
from .trx import register_trx


async def init_all_owner(client):
    """
    Inisialisasi OWNER_ID (cukup sekali dari commands.py).
    """
    await init_owner(client)


def init(client):
    """
    Daftarkan semua perintah dari folder perintah.
    """
    register_commands(client)
    register_trx(client)
