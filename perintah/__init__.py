import importlib
import pkgutil

# Dictionary global untuk menampung semua HELP dari tiap modul
HELP = {}

def init(client):
    package = __name__

    for _, module_name, ispkg in pkgutil.iter_modules(__path__):
        if ispkg:
            continue

        try:
            # Import modul
            module = importlib.import_module(f"{package}.{module_name}")

            # Jalankan fungsi register(client) kalau ada
            if hasattr(module, "register"):
                module.register(client)
                print(f"✅ Modul perintah dimuat: {module_name}")
            else:
                print(f"⚠️ Modul {module_name} tidak punya fungsi register()")

            # Gabungkan HELP kalau ada
            if hasattr(module, "HELP"):
                for k, v in module.HELP.items():
                    if k not in HELP:
                        HELP[k] = []
                    HELP[k].extend(v)

        except Exception as e:
            print(f"❌ Gagal load modul {module_name}: {e}")
