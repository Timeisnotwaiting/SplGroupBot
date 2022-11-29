from pyrogram import Client, filters
from config import CHATS
from config import DEV

DEV_USERS = DEV.SUDO_USERS + [DEV.OWNER_ID]

DUMP = CHATS.LOG_GROUP_ID

VALID_WELCOME_FORMATTERS = [
    "first",
    "last",
    "fullname",
    "username",
    "id",
    "count",
    "chatname",
    "mention",
]

@Client.on_message(filters.command("setwelcome") & filters.group)
async def welcome_setter(_, m):
    id = m.from_user.id
    if not id in DEV_USERS:
        x = await _.get_chat_member(m.chat.id, id)
        if not x.privileges:
            return
        if not x.privileges.can_change_info:
            return await m.reply(f"**You can't change welcome settings !**")
    if not m.reply_to_message:
        return await m.reply(f"**Reply to a message...**")
    await _.copy_message(DUMP, m.chat.id, m.reply_to_message.id)
    await set_welcome(m.chat.id, m.reply_to_message.id)
    await m.reply("**Welcome message has been saved**")