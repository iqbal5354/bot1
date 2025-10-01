import speedtest
from telethon import events

OWNER_ID = None

async def init_owner_speed(client):
    global OWNER_ID
    me = await client.get_me()
    OWNER_ID = me.id


def register_speedtest(client):
    @client.on(events.NewMessage(pattern=r"^\.speedtest$"))
    async def handler_speed(event):
        await event.edit("⚡ Menjalankan speedtest, tunggu sebentar...")
        try:
            s = speedtest.Speedtest()
            s.get_best_server()
            s.download()
            s.upload()
            result = s.results.dict()

            msg = (
                "📊 **Hasil Speedtest**\n\n"
                f"🌍 Server: {result['server']['sponsor']} ({result['server']['name']})\n"
                f"🏓 Ping: {result['ping']} ms\n"
                f"⬇️ Download: {result['download']/1_000_000:.2f} Mbps\n"
                f"⬆️ Upload: {result['upload']/1_000_000:.2f} Mbps\n"
            )
            await event.edit(msg)
        except Exception as e:
            await event.edit(f"❌ Error speedtest: {str(e)}")
