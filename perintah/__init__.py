import importlib
import pkgutil

# Dictionary global untuk menampung semua HELP dari tiap modul
HELP = {}

def init(client):
    # Cari semua modul di dalam package ini (perintah/)
    package = __name__
    for _, module_name, ispkg in pkgutil.iter_modules(__path__):
        if ispkg:
            continue

        # Skip file init
        if module_name == "__init__":
            continue

        try:
            # Import modul
            module = importlib.import_module(f"{package}.{module_name}")

            # Jalankan fungsi register(client) kalau ada
            if hasattr(module, "register"):
                module.register(client)

            # Gabungkan HELP kalau ada
            if hasattr(module, "HELP"):
                for k, v in module.HELP.items():
                    if k not in HELP:
                        HELP[k] = []
                    HELP[k].extend(v)

            print(f"✅ Modul perintah dimuat: {module_name}")

        except Exception as e:
            print(f"❌ Gagal load modul {module_name}: {e}")
