from pyrogram import filters
from pyrogram.types import Message

from config import BANNED_USERS
from strings import get_command
from ZeebMusic import app
from ZeebMusic.misc import SUDOERS
from ZeebMusic.utils.database import blacklist_chat, blacklisted_chats, whitelist_chat
from ZeebMusic.utils.decorators.language import language

# Commands

BLACKLISTCHAT_COMMAND = get_command("BLACKLISTCHAT_COMMAND")
WHITELISTCHAT_COMMAND = get_command("WHITELISTCHAT_COMMAND")
BLACKLISTEDCHAT_COMMAND = get_command("BLACKLISTEDCHAT_COMMAND")


@app.on_message(filters.command(BLACKLISTCHAT_COMMAND) & SUDOERS)
@language
async def blacklist_chat_func(client, message: Message, _):
    if len(message.command) != 2:
        return await message.reply_text(_["black_1"])
    chat_id = int(message.text.strip().split()[1])
    if chat_id in await blacklisted_chats():
        return await message.reply_text(_["black_2"])
    blacklisted = await blacklist_chat(chat_id)
    if blacklisted:
        await message.reply_text(_["black_3"])
    else:
        await message.reply_text("sᴏᴍᴇᴛʜɪɴɢ ᴡʀᴏɴɢ ʜᴀᴘᴘᴇɴᴇᴅ.")
    try:
        await app.leave_chat(chat_id)
    except:
        pass


@app.on_message(filters.command(WHITELISTCHAT_COMMAND) & SUDOERS)
@language
async def white_funciton(client, message: Message, _):
    if len(message.command) != 2:
        return await message.reply_text(_["black_4"])
    chat_id = int(message.text.strip().split()[1])
    if chat_id not in await blacklisted_chats():
        return await message.reply_text(_["black_5"])
    whitelisted = await whitelist_chat(chat_id)
    if whitelisted:
        return await message.reply_text(_["black_6"])
    await message.reply_text("sᴏᴍᴇᴛʜɪɴɢ ᴡʀᴏɴɢ ʜᴀᴘᴘᴇɴᴇᴅ.")


@app.on_message(filters.command(BLACKLISTEDCHAT_COMMAND) & ~BANNED_USERS)
@language
async def all_chats(client, message: Message, _):
    text = _["black_7"]
    j = 0
    for count, chat_id in enumerate(await blacklisted_chats(), 1):
        try:
            title = (await app.get_chat(chat_id)).title
        except Exception:
            title = "ᴘʀɪᴠᴀᴛᴇ"
        j = 1
        text += f"**{count}. {title}** [`{chat_id}`]\n"
    if j == 0:
        await message.reply_text(_["black_8"])
    else:
        await message.reply_text(text)
