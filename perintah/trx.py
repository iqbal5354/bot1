from telethon import events

def init(client):
    @client.on(events.NewMessage(pattern=r"^\.isi$"))
    async def handler_isi(event):
        text = (
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
        await event.respond(text)

    @client.on(events.NewMessage(pattern=r"^\.danamasuk$"))
    async def handler_danamasuk(event):
        text = (
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
        await event.respond(text)
