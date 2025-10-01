from telethon import events

OWNER_ID = None

async def init_owner(client):
    global OWNER_ID
    me = await client.get_me()
    OWNER_ID = me.id


def register_trx(client):
    @client.on(events.NewMessage(pattern=r"^\.isi$"))
    async def handler_isi(event):
        await event.edit(
            "Jika sudah sepakat #DONE\n\n"
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
    async def handler_danamasuk(event):
        await event.edit(
            "**:: Uang sudah masuk di saya. Silahkan kalian serah terima data ::**\n\n"
            "```\n"
            "━━━━━━━━PENTING!!━━━━━━━━\n"
            "⚠️Harap Tanyakan dulu masalah Garansi.\n"
            "⚠️Jgn coba2 ada drama jika tidak mau saya mintain ident via VC.\n"
            "⚠️Jangan Berikan OTP tele/WA/email di luar transaksi.\n"
            "⚠️Jika Pembeli tidak ada kabar 8 jam = dana cair,\n"
            "   Jika Penjual hilang 5 jam = uang balik ke pembeli\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "```\n"
        )

    @client.on(events.NewMessage(pattern=r"^\.format$"))
    async def handler_format(event):
        await event.edit(
            "**FORMAT TRANSAKSI**\n\n"
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
    async def handler_aturan(event):
        await event.edit(
            "Selamat Datang di Rekber Warung Bullove\n\n"
            "Mohon untuk dibaca dan diperhatikan\n"
            "```——————————————————————————————————```\n"
            "**PERATURAN REKBER :**\n"
            "1. Pastikan saya admin Grub Rekber.\n"
            "2. Dilarang Kick Penjual/pembeli & Ganti Judul.\n"
            "3. Tidak menerima REKBER barang/jasa iLEGAL.\n"
            "4. Mohon untuk jujur mengisi judul TRX!\n\n"
            "❗Jika Pembeli tidak ada kabar 8 jam = dana cair,\n"
            "❗Jika Penjual hilang 5 jam = uang balik ke pembeli.\n"
            "❗Cancel tetap potong fee.\n"
            "❗Transaksi akun wajib take seEMAIL.\n"
            "❗Jangan berikan OTP tele/WA/email di luar transaksi.\n"
            "❗Seller/Buyer dilarang hilang selama transaksi.\n\n"
            "®️𝙒𝙖𝙧𝙪𝙣𝙜 𝘽𝙪𝙡𝙡𝙤𝙫𝙚"
        )
