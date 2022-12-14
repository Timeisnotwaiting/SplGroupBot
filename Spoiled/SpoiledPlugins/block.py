from config import DEV
from Spoiled.Database.blocked import *
from pyrogram import Client, filters
from pyrogram.types import Message

SUDOERS = DEV.SUDO_USERS + [DEV.OWNER_ID]

@Client.on_message(filters.command(["block", "unblock"]))
async def bloblo(_, m: Message):
    if m.from_user.id not in SUDOERS:
        return
    replied = m.reply_to_message
    if replied:
        a = m.reply_to_message.from_user.id
    elif replied and len(m.command) > 1:
        a = m.reply_to_message.from_user.id
    elif (not replied and len(m.command) > 1):
        xD = m.text.split()
        try:
            a = int(xD[1])
        except:
            await m.reply("please enter id only")
    else:
        await m.reply("Try /block | /unblock [ reply | id ]")
    if a in SUDOERS:
        return await m.reply("you can't block the owner of this bot !")

    if m.text.split()[0][1].lower() == "u":
        blocked = await is_blocked(a)
        if blocked:
            await unblock(a)
            await m.reply("user unblocked")
    else:
        blocked = await is_blocked(a)
        if not blocked:
            await block(a)
            await m.reply("user blocked")
    
