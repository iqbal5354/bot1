import importlib
import pkgutil
import inspect
from telethon import events
from bot import OWNER_ID  # ambil OWNER_ID dari bot.py

# Dictionary global untuk menampung semua HELP dari tiap modul
HELP = {}

async def init(client):
    # 🛡️ Filter global: hanya OWNER_ID yang bisa pakai perintah
    @client.on(events.NewMessage)
    async def global_owner_filter(event):
        if event.sender_id != OWNER_ID:
            event._handled = True  # hentikan propagasi event ke handler lain
            return

    package = __name__

    for _, module_name, ispkg in pkgutil.iter_modules(__path__):
        if ispkg:
            continue

        try:
            module = importlib.import_module(f"{package}.{module_name}")

            # 🔹 Jalankan init(client) kalau ada
            if hasattr(module, "init"):
                module.init(client)
                print(f"✅ Modul {module_name} dimuat via init()")

            # 🔹 Jalankan register(client) kalau ada
            if hasattr(module, "register"):
                module.register(client)
                print(f"✅ Modul {module_name} dimuat via register()")

            # 🔹 Jalankan init_owner(client) kalau ada
            if hasattr(module, "init_owner"):
                func = module.init_owner
                if inspect.iscoroutinefunction(func):
                    try:
                        await func(client)
                    except Exception as e:
                        print(f"⚠️ Modul {module_name} gagal init_owner(): {e}")
                else:
                    try:
                        func(client)
                    except Exception as e:
                        print(f"⚠️ Modul {module_name} gagal init_owner(): {e}")
                print(f"✅ Modul {module_name} dimuat via init_owner()")

            # 🔹 Gabungkan HELP kalau ada
            if hasattr(module, "HELP"):
                for k, v in module.HELP.items():
                    if k not in HELP:
                        HELP[k] = []
                    HELP[k].extend(v)

        except Exception as e:
            print(f"❌ Gagal load modul {module_name}: {e}")
