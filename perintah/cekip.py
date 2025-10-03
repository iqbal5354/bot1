import requests
from pyrogram import Client, filters

@Client.on_message(filters.command("cekip", prefixes=".") & filters.private)
async def cekip(client, message):
    try:
        # ambil IP publik
        ip = requests.get("https://api.ipify.org").text

        # ambil detail lokasi/region
        info = requests.get(f"https://ipinfo.io/{ip}/json").json()
        lokasi = info.get("city", "Unknown") + ", " + info.get("region", "Unknown")
        negara = info.get("country", "Unknown")

        await message.reply_text(
            f"🌐 **Info Server Bot**\n\n"
            f"📡 IP Publik: `{ip}`\n"
            f"🏙️ Lokasi: {lokasi}\n"
            f"🇺🇳 Negara: {negara}"
        )
    except Exception as e:
        await message.reply_text(f"❌ Gagal cek IP\nError: {e}")
