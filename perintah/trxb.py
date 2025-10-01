from telethon import events, Button

HELP = {
    "trx": [
        ".isi → format rekening",
        ".danamasuk → konfirmasi uang masuk",
        ".format → format transaksi",
        ".aturan → peraturan rekber"
    ]
}

def init(client):

    # 📌 Tombol khusus TRX
    @client.on(events.NewMessage(pattern=r"^\.trxb$"))
    async def trx_menu(event):
        buttons = [
            [Button.inline("📋 Isi", data="trx_isi")],
            [Button.inline("💰 Dana Masuk", data="trx_danamasuk")],
            [Button.inline("📝 Format", data="trx_format")],
            [Button.inline("📜 Aturan", data="trx_aturan")],
        ]
        await event.respond("📖 **Menu TRX**\nPilih perintah:", buttons=buttons)

    @client.on(events.CallbackQuery)
    async def trx_callback(event):
        data = event.data.decode("utf-8")

        if data == "trx_isi":
            await event.edit(
                "Jika sudah sepakat #DONE\n\n"
                "Penjual Silahkan Di isi :\n\n"
                "Klik 1x text kutipan di bawah untuk COPY\n"
                "```\n"
                "——————————————————————————————————\n"
                " Nama Bank/ewallet :\n"
                " Atas Nama         :\n"
                " No Rek            :\n"
                "——————————————————————————————————\n"
                "```\n"
                "Nb:\n"
                "Biaya admin bank ditanggung oleh pencair.",
                link_preview=False,
                buttons=[[Button.inline("⬅️ Back", data="trx_back")]]
            )

        elif data == "trx_danamasuk":
            await event.edit(
                "**:: Uang sudah masuk di saya. Silahkan kalian serah terima data ::**\n\n"
                "```\n"
                "━━━━━━━━PENTING!!━━━━━━━━\n"
                "⚠️ Harap tanyakan dulu masalah garansi.\n"
                "⚠️ Jangan ada drama, jika ada = saya minta ident via VC.\n"
                "⚠️ Jangan berikan OTP (tele/WA/email) di luar transaksi.\n"
                "⚠️ Jika pembeli tidak ada kabar 8 jam → dana cair.\n"
                "⚠️ Jika penjual hilang 5 jam → uang balik ke pembeli.\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                "```",
                link_preview=False,
                buttons=[[Button.inline("⬅️ Back", data="trx_back")]]
            )

        elif data == "trx_format":
            await event.edit(
                "**FORMAT TRANSAKSI**\n\n"
                "Klik 1x text kutipan dibawah untuk COPY format:\n"
                "```\n"
                "Transaksi Apa  :\n"
                "Penjual Siapa  :\n"
                "Pembeli Siapa  :\n"
                "Harga Berapa   :\n"
                "Fee: Buyer/seller\n"
                "```\n\n"
                "Nb:\n"
                "- Tanyakan ulang masalah garansi\n"
                "- Tanyakan ulang kesepakatan DONE\n"
                "- CANCEL/BATAL → FEE tetap terpotong!",
                link_preview=False,
                buttons=[[Button.inline("⬅️ Back", data="trx_back")]]
            )

        elif data == "trx_aturan":
            await event.edit(
                "Selamat Datang di Rekber Warung Bullove\n\n"
                "Mohon untuk dibaca dan diperhatikan\n"
                "```——————————————————————————————————```\n"
                "**PERATURAN REKBER :**\n"
                "1. Pastikan saya admin Grub Rekber.\n"
                "2. Dilarang Kick Penjual/Pembeli & ganti judul.\n"
                "3. Tidak menerima REKBER barang/jasa ilegal.\n"
                "4. Mohon untuk jujur mengisi judul TRX!\n\n"
                "**KETENTUAN TRANSAKSI :**\n"
                "❗ Pembeli hilang 8 jam → dana cair.\n"
                "❗ Penjual hilang 5 jam → uang balik ke pembeli.\n"
                "❗ Cancel tetap kena potong fee.\n"
                "❗ Transaksi akun wajib take seEMAIL.\n"
                "❗ Jangan berikan OTP (tele/WA/email) di luar transaksi.\n"
                "❗ Seller & Buyer dilarang hilang saat transaksi.\n\n"
                "®️ 𝙒𝙖𝙧𝙪𝙣𝙜 𝘽𝙪𝙡𝙡𝙤𝙫𝙚",
                link_preview=False,
                buttons=[[Button.inline("⬅️ Back", data="trx_back")]]
            )

        elif data == "trx_back":
            buttons = [
                [Button.inline("📋 Isi", data="trx_isi")],
                [Button.inline("💰 Dana Masuk", data="trx_danamasuk")],
                [Button.inline("📝 Format", data="trx_format")],
                [Button.inline("📜 Aturan", data="trx_aturan")],
            ]
            await event.edit("📖 **Menu TRX**\nPilih perintah:", buttons=buttons)
