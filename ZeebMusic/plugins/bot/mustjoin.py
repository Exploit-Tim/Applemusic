from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from pyrogram.errors import ChatAdminRequired, UserNotParticipant, ChatWriteForbidden
from ZeebMusic import app

#--------------------------

MUST_JOIN = "SpotifyStream_Id"
#------------------------
@app.on_message(filters.incoming & filters.private, group=-1)
async def must_join_channel(app: Client, msg: Message):
    if not MUST_JOIN:
        return
    try:
        try:
            await app.get_chat_member(MUST_JOIN, msg.from_user.id)
        except UserNotParticipant:
            if MUST_JOIN.isalpha():
                link = "https://t.me/" + MUST_JOIN
            else:
                chat_info = await app.get_chat(MUST_JOIN)
                link = chat_info.invite_link
            try:
                await msg.reply_photo(
                    photo="https://mallucampaign.in/images/img_1710090490.jpg", caption=f"<blockquote><b>Silahkan bergabung dulu [Support]({link}) ,jika ingin menggunakan bot ini, jika sudah bergabung silahkan ulangi /start</b></blockquote>",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton("🎵 JOIN DULU", url="https://t.me/SpotifyStream_Id"),
                            ]
                        ]
                    )
                )
                await msg.stop_propagation()
            except ChatWriteForbidden:
                pass
    except ChatAdminRequired:
        print(f"Promosi saya sebagai admin digrup/channels yang diFSUB: {MUST_JOIN} !")
