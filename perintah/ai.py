import os
import openai
from telethon import events

OWNER_ID = None  # nanti diisi otomatis dari init_owner

# ambil API key
openai.api_key = os.getenv("OPENAI_API_KEY")

def register_ai(client):
    # 📌 .ai <pertanyaan>
    @client.on(events.NewMessage(pattern=r"^\.ai (.+)"))
    async def handler_ai(event):
        if event.sender_id != OWNER_ID:  # optional, bisa dihapus kalau semua boleh
            return

        tanya = event.pattern_match.group(1)
        msg = await event.reply("🤖 Sedang berpikir...")

        try:
            resp = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": tanya}],
                max_tokens=300,
                temperature=0.7,
            )
            jawaban = resp["choices"][0]["message"]["content"]
            await msg.edit(f"💡 **Jawaban AI:**\n{jawaban}")
        except Exception as e:
            await msg.edit(f"❌ Error AI: {str(e)}")
