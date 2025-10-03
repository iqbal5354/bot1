import aiohttp
from telethon import events

HELP = {
    "utility": [
        ".ip → cek IP & region server bot",
    ]
}

def register(client):
    # 📌 .ip
    @client.on(events.NewMessage(pattern=r"^\.ip$"))
    async def handler_ip(event):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get("https://ipinfo.io/json") as resp:
                    res = await resp.json()

            ip = res.get("ip", "Unknown")
            city = res.get("city", "Unknown")
            region = res.get("region", "Unknown")
            country = res.get("country", "Unknown")
            org = res.get("org", "Unknown")

            await event.edit(
                f"🌐 **IP Info**\n\n"
                f"🔹 IP: `{ip}`\n"
                f"🏙 City: {city}\n"
                f"📍 Region: {region}\n"
                f"🌍 Country: {country}\n"
                f"🏢 ISP: {org}"
            )
        except Exception as e:
            await event.edit(f"❌ Gagal ambil info IP: {e}")
