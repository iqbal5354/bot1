from telethon import events

def init_trx(client):

    @client.on(events.NewMessage(pattern=r"^\.isi$"))
    async def isi_handler(event):
        await event.respond(
            "Jika sudah sepakat #DONE\n"
            "Penjual Silahkan Di isi :\n\n"
            "klik  1x text kutipan di bawah untuk COPY\n"
            "```\n"
            "——————————————————————————————————\n"
            " Nama Bank/ewallet :\n"
            " Atas Nama         :\n"
            " No Rek            :\n"
            "——————————————————————————————————\n"
            "```\n"
            "Nb:\n"
            "Biaya admin bank ditanggung oleh pencair."
        )

    @client.on(events.NewMessage(pattern=r"^\.danamasuk$"))
    async def danamasuk_handler(event):
        await event.respond(
            "**:: Uang sudah masuk di saya. Silahkan kalian serah terima data ::**\n\n"
            "```\n"
            "━━━━━━━━PENTING!!━━━━━━━━\n"
            "⚠️Harap Tanyakan dulu masalah Garansi.\n"
            "⚠️Jgn coba2 ada drama jika tidak mau saya mintain ident via VC. Karena drama=ripper.\n"
            "⚠️Jangan Berikan Hal2 yg rawan seperti OTP tele WA OTP email di luar transaksi\n"
            "⚠️jika Pembeli tidak ada kabar selama 8 jam maka dana akan di cairkan dan jika penjual tidak ada kabar selama 5 jam uang di transfer balik ke pembeli\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "```\n"
        )

    @client.on(events.NewMessage(pattern=r"^\.format$"))
    async def format_handler(event):
        await event.respond(
            "**FORMAT TRANSAKSI\n\n**"
            "Klik 1x text kutipan dibawah untuk COPY format\n"
            "```\n"
            "Transaksi Apa  :\n"
            "Penjual Siapa  :\n"
            "Pembeli Siapa  :\n"
            "Harga Berapa   :\n"
            "Fee: Buyer/seller\n"
            "```\n\n"
            "Nb:\n"
            "-Tanyakan ulang masalah garansi\n"
            "-Tanyakan ulang kesepakatan DONE\n"
            "-CANCEL/BATAL FEE TETAP TERPOTONG!"
        )

    @client.on(events.NewMessage(pattern=r"^\.aturan$"))
    async def aturan_handler(event):
        await event.respond(
            "Selamat Datang di Rekber Warung Bullove\n\n"
            "Mohon untuk dibaca dan diperhatikan\n"
            "```——————————————————————————————————```\n"
            "**PERATURAN REKBER :**\n"
            "1. Pastikan saya admin Grub Rekber.\n"
            "2. Dilarang Kick Penjual/pembeli & Ganti Judul.\n"
            "3. Tidak menerima REKBER barang/jasa iLEGAL (melanggar UUD)!\n"
            "4. Mohon untuk jujur mengisi judul TRX!\n\n"
            "**KETENTUAN TRANSAKSI :**\n"
            "❗️Jika Pembeli tidak ada kabar selama 8 jam maka dana akan dicairkan, dan jika penjual tidak ada kabar selama 5 jam uang akan ditransfer balik ke pembeli.\n"
            "❗️Jika Transaksi **Cancel/BATAL** Fee tetap Terpotong, jika tdk mau Terpotong Silahkan cari penjual lain.\n"
            "❗️Transaksi akun wajib take seEMAILnya agar tidak kena HB.\n"
            "❗️Jangan berikan hal2 yg rawan seperti OTP tele, WA, OTP email (di luar transaksi).\n"
            "❗️INGAT SELLER MAUPUN BUYER DILARANG MENGHILANG SELAMA TRANSAKSI!\n"
            "❗️Harap tanyakan dulu masalah Garansi.\n\n"
            "**Nb :**\n"
            "🔜 Admin tidak pernah merekomendasiin siapapun\n"
            "🔜 Berani drama selama transaksi maka admin wajib meminta ident kalian berdua️\n"
            "🔜 MENYALAHGUNAKAN TRANSAKSI UNTUK PENIPUAN/TRANSAKSI PALSU AKAN KAMI SERAHKAN KEPADA PIHAK YG BERWAJIB\n"
            "```——————————————————————————————————```\n"
            "Jika Setuju Silahkan Pembeli isi Format Transaksi ✔️\n\n"
            "®️𝙒𝙖𝙧𝙪𝙣𝙜 𝘽𝙪𝙡𝙡𝙤𝙫𝙚"
        )
