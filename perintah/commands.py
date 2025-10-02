import sys
import os
import time
import asyncio
import random
from telethon import events
from telethon.tl.functions.channels import CreateChannelRequest
from telethon.tl.functions.messages import CreateChatRequest, ExportChatInviteRequest
from telethon.errors import FloodWaitError

HELP = {
    "utility": [
        ".ping → cek respon bot",
        ".id → cek ID grup/channel",
        ".restart → restart bot",
    ]
}

OWNER_ID = None

# === RANDOM MESSAGES ===
RANDOM_MESSAGES = [
    "Hari ini penuh kejutan, semoga energi positif selalu hadir di setiap langkah yang kita jalani bersama di sini.",
    "Grup ini dibuat untuk berbagi cerita, pengalaman, dan tawa yang bisa menghibur kita semua setiap hari tanpa henti.",
    "Kebersamaan adalah kunci, mari kita bangun komunitas ini dengan saling menghargai dan memberi semangat positif.",
    "Semoga tempat ini jadi ruang yang nyaman untuk berdiskusi, bercanda, dan saling menguatkan satu sama lain setiap waktu.",
    "Jangan sungkan untuk berbagi ide, opini, maupun hal-hal kecil yang bisa bikin suasana grup jadi lebih hidup.",
    "Hidup terlalu singkat untuk saling diam, mari kita manfaatkan kesempatan ini untuk saling menyapa dan berteman baik.",
    "Setiap orang punya cerita unik, semoga grup ini bisa jadi wadah untuk kita saling mengenal lebih dalam lagi.",
    "Selamat datang di rumah baru kita, mari isi ruang ini dengan candaan, obrolan hangat, dan juga semangat positif.",
    "Tidak ada pertemuan yang kebetulan, semoga kita bisa menjadikan tempat ini penuh manfaat dan pengalaman berharga.",
    "Bersama kita bisa membangun lingkungan yang lebih menyenangkan, penuh tawa, dan saling mendukung setiap anggota.",
    "Grup ini terbuka untuk siapa saja yang ingin berbagi pikiran, cerita lucu, atau sekadar menyapa dengan ramah.",
    "Setiap kata yang kita bagikan bisa jadi energi positif bagi orang lain, jadi mari sebarkan hal baik di sini.",
    "Terima kasih sudah menjadi bagian dari perjalanan ini, semoga grup ini bisa memberi kesan yang menyenangkan.",
    "Mari gunakan ruang ini untuk mengekspresikan diri, tanpa rasa takut, dengan penuh kebebasan dan kebersamaan.",
    "Tak peduli seberapa jauh jarak memisahkan, semoga grup ini bisa jadi penghubung persahabatan yang hangat.",
    "Hidup lebih indah kalau dibagi bersama, mari kita jadikan grup ini tempat untuk saling berbagi kebahagiaan.",
    "Kita semua punya tujuan berbeda, tapi mari kita satukan semangat agar ruang ini bermanfaat dan menyenangkan.",
    "Jangan malu untuk aktif, semakin banyak obrolan semakin hangat suasana yang bisa kita rasakan bersama-sama.",
    "Obrolan santai, diskusi serius, atau sekadar bercanda, semuanya bisa hidup di sini dengan sikap saling menghargai.",
    "Setiap awal pasti punya cerita baru, semoga grup ini jadi awal dari kisah-kisah seru yang akan kita jalani.",
    "Mari kita isi hari-hari dengan cerita menarik, canda, tawa, dan kehangatan yang bisa menyemangati semuanya.",
    "Setiap anggota adalah bagian penting, mari kita saling dukung agar grup ini tumbuh jadi komunitas yang solid.",
    "Jangan ragu untuk menyapa, satu pesan kecil bisa membuka obrolan panjang yang bikin kita makin akrab.",
    "Semoga grup ini bisa jadi tempat bertukar pikiran yang sehat, menyenangkan, dan penuh hal positif setiap hari.",
    "Tidak ada kata bosan kalau kita bisa saling menghibur, semoga grup ini jadi ruang untuk tawa yang menyegarkan.",
    "Mari hargai setiap perbedaan, karena perbedaanlah yang membuat grup ini lebih berwarna dan penuh makna.",
    "Tak ada batasan untuk berbagi cerita, semoga setiap percakapan bisa membawa kebahagiaan bagi kita semua.",
    "Komunitas ini tercipta karena rasa ingin bersama, mari kita jaga suasana tetap hangat dan penuh keceriaan.",
    "Obrolan sederhana kadang bisa jadi kenangan indah, semoga grup ini menyimpan banyak kisah yang kita kenang.",
    "Selamat datang di awal perjalanan, semoga kita semua betah berada di sini dan aktif berbagi cerita seru."
]


# === OWNER INIT ===
async def init_owner(client):
    global OWNER_ID
    me = await client.get_me()
    OWNER_ID = me.id
    print(f"ℹ️ OWNER_ID otomatis diset ke: {OWNER_ID} ({me.username or me.first_name})")
    try:
        await client.send_message(OWNER_ID, "✅ Bot berhasil dijalankan dan siap dipakai.")
    except Exception:
        pass


# === HELPERS ===
def progress_bar(current, total, length=20):
    filled = int(length * current // total)
    bar = "█" * filled + "▒" * (length - filled)
    return f"[{bar}] {current}/{total}"


async def animate_loading(msg, text, delay=0.3):
    frames = ["⏳", "⌛", "🔄", "🌀", "⚙️"]
    for frame in frames:
        await msg.edit(f"{frame} {text}")
        await asyncio.sleep(delay)


# === COMMANDS ===
def register_commands(client):

    # 📌 .ping
    @client.on(events.NewMessage(pattern=r"^\.ping$"))
    async def handler_ping(event):
        start = time.perf_counter()
        await event.edit("🏓 Pong...")
        end = time.perf_counter()
        ping_ms = int((end - start) * 1000)
        await event.edit(f"🏓 Pong!\n⏱ {ping_ms} ms")

    # 📌 .id
    @client.on(events.NewMessage(pattern=r"^\.id$"))
    async def handler_id(event):
        chat = await event.get_chat()
        chat_id = chat.id
        if not str(chat_id).startswith("-100") and (event.is_group or event.is_channel):
            chat_id = f"-100{abs(chat_id)}"
        await event.edit(f"🆔 Chat ID: {chat_id}")

    # 📌 .buat
    @client.on(events.NewMessage(pattern=r"^\.buat (b|g|c)(?: (\d+))? (.+)"))
    async def handler_buat(event):
        if event.sender_id != OWNER_ID:
            return

        await event.delete()  # hapus command asli
        jenis = event.pattern_match.group(1)
        jumlah = int(event.pattern_match.group(2)) if event.pattern_match.group(2) else 1
        nama = event.pattern_match.group(3)

        msg = await event.respond("⏳ Menyiapkan pembuatan group/channel...")

        try:
            hasil = []
            for i in range(1, jumlah + 1):
                nama_group = f"{nama} {i}" if jumlah > 1 else nama

                await animate_loading(msg, f"Membuat {nama_group} ({i}/{jumlah})")

                if jenis == "b":
                    r = await client(CreateChatRequest(
                        users=[await client.get_me()],
                        title=nama_group,
                    ))
                    chat_id = r.chats[0].id
                else:
                    r = await client(CreateChannelRequest(
                        title=nama_group,
                        about="GRUB BY @WARUNGBULLOVE",
                        megagroup=(jenis == "g"),
                    ))
                    chat_id = r.chats[0].id

                # link undangan
                link = (await client(ExportChatInviteRequest(chat_id))).link
                hasil.append(f"✅ [{nama_group}]({link})")

                # 🔹 kirim 4 pesan random otomatis
                for _ in range(4):
                    pesan = random.choice(RANDOM_MESSAGES)
                    try:
                        await client.send_message(chat_id, pesan)
                        await asyncio.sleep(1)
                    except FloodWaitError as fw:
                        await asyncio.sleep(fw.seconds)
                        await client.send_message(chat_id, pesan)

                bar = progress_bar(i, jumlah)
                await msg.edit(f"🔄 Membuat group/channel...\n{bar}")

            await msg.edit("🎉 Grup/Channel berhasil dibuat:\n\n" + "\n".join(hasil), link_preview=False)

        except FloodWaitError as e:
            await msg.edit(f"⚠️ Kena limit Telegram!\nTunggu {e.seconds//3600} jam {e.seconds%3600//60} menit.")
        except Exception as e:
            await msg.edit(f"❌ Error: {str(e)}")

    # 📌 .restart
    @client.on(events.NewMessage(pattern=r"^\.restart$"))
    async def handler_restart(event):
        if event.sender_id != OWNER_ID:
            return
        await event.edit("♻️ Bot sedang restart...")
        args = [sys.executable] + sys.argv
        os.execv(sys.executable, args)


# Panggil fungsi ini di bot.py setelah client dibuat
def init(client):
    register_commands(client)
