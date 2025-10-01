import os
import time
import speedtest
from telethon import events

OWNER_ID = None

async def init_owner_speed(client):
    """
    Ambil OWNER_ID otomatis untuk modul speedtest.
    """
    global OWNER_ID
    me = await client.get_me()
    OWNER_ID = me.id

def register_speedtest(client):
    # 📌 .speedtest
    @client.on(events.NewMessage(pattern=r"^\.speedtest$"))
    async def handler_speedtest(event):
        if OWNER_ID and event.sender_id != OWNER_ID:
            return  # hanya owner

        msg = await event.reply("🚀 Menjalankan speedtest... Tunggu sebentar.")

        try:
            st = speedtest.Speedtest()
            st.get_best_server()
            download_speed = st.download()
            upload_speed = st.upload()
            ping_result = st.results.ping

            # Ubah ke Mbps
            download_mbps = download_speed / 1_000_000
            upload_mbps = upload_speed / 1_000_000

            result = (
                "📊 **Hasil Speedtest**\n\n"
                f"⚡ Ping: `{ping_result:.2f} ms`\n"
                f"⬇️ Download: `{download_mbps:.2f} Mbps`\n"
                f"⬆️ Upload: `{upload_mbps:.2f} Mbps`\n"
            )
            await msg.edit(result)

        except Exception as e:
            await msg.edit(f"❌ Error speedtest: {str(e)}")
