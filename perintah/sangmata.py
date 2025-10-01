import asyncio
from telethon import events, types
from telethon.errors.rpcerrorlist import YouBlockedUserError

OWNER_ID = None

async def init_owner(client):
    global OWNER_ID
    me = await client.get_me()
    OWNER_ID = me.id


def mentionuser(name, user_id):
    return f"[{name}](tg://user?id={user_id})"


def sanga_seperator(responses):
    names = []
    usernames = []
    for resp in responses:
        if "Name" in resp:
            names.append(resp)
        elif "Username" in resp:
            usernames.append(resp)
    return ("\n".join(names) or "`Tidak ada riwayat nama.`",
            "\n".join(usernames) or "`Tidak ada riwayat username.`")


def init(client):

    @client.on(events.NewMessage(pattern=r"^\.sg(u)?(?:\s|$)(.*)"))
    async def sangmata(event):
        """
        📌 Cek history nama/username lewat @SangMata_beta_bot
        • .sg <reply/userid/username>
        • .sgu <reply/userid/username>
        """
        cmd = event.pattern_match.group(1)   # "" = nama, "u" = username
        user = event.pattern_match.group(2)  # target (id/username)

        reply = await event.get_reply_message()
        if not user and reply:
            user = str(reply.sender_id)

        if not user:
            await event.edit("⚠️ Reply pesan user atau masukkan userid/username")
            await asyncio.sleep(5)
            return await event.delete()

        # Ambil entitas user
        try:
            if user.isdigit():
                userinfo = await client.get_entity(int(user))
            else:
                userinfo = await client.get_entity(user)
        except ValueError:
            await event.edit("❌ Tidak bisa fetch user.")
            return

        if not isinstance(userinfo, types.User):
            await event.edit("❌ Target bukan user valid.")
            return

        await event.edit("⏳ Memproses...")

        responses = []
        try:
            async with client.conversation("@SangMata_beta_bot") as conv:
                try:
                    await conv.send_message(str(userinfo.id))
                except YouBlockedUserError:
                    await event.edit("⚠️ Kamu block @SangMata_beta_bot, unblock dulu!")
                    return

                while True:
                    try:
                        response = await conv.get_response(timeout=2)
                    except asyncio.TimeoutError:
                        break
                    responses.append(response.text)

                await client.send_read_acknowledge(conv.chat_id)
        except Exception as e:
            await event.edit(f"❌ Error: {str(e)}")
            return

        if not responses:
            await event.edit("❌ Tidak ada hasil dari @SangMata_beta_bot")
            return

        if any("No records found" in r or "No data available" in r for r in responses):
            await event.edit("ℹ️ User ini tidak punya riwayat.")
            return

        names, usernames = sanga_seperator(responses)
        check = (usernames, "Username") if cmd == "u" else (names, "Nama")

        nama_user = f"{userinfo.first_name} {userinfo.last_name}" if userinfo.last_name else userinfo.first_name
        output = f"👤 **User:** {mentionuser(nama_user, userinfo.id)}\n📜 **Riwayat {check[1]}:**\n{check[0]}"

        await event.edit(output, link_preview=False)


# 📌 Help section supaya auto kebaca di .help
__HELP__ = """
**Sangmata Tools**
`.sg <reply/userid/username>` → cek riwayat **nama**
`.sgu <reply/userid/username>` → cek riwayat **username**
"""
