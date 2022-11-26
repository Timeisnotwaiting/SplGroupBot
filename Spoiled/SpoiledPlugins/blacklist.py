from pyrogram import Client, filters
from Spoiled.Database.blacklist import *
from config import DEV

DEV_USERS = [DEV.OWNER_ID] + DEV.SUDO_USERS

@Client.on_message(filters.command(["addblacklist", "addblocklist"]))
async def blacklist(_, m):
    if not m.from_user.id in DEV_USERS:
        x = await _.get_chat_member(m.chat.id, m.from_user.id)
        if not x.status in ["creator", "administrator"]:
            return await m.reply("Only admin can perform this action !")
    if not len(m.command) > 1:
        return await m.reply("`/addblacklist < word > `")
    word = m.text.split()[1] 
    check = await is_blacklist(m.chat.id, word)
    if check:
        return await m.reply(f"`{word}` is already blacklisted !")
    await add_blacklist(m.chat.id, word)
    await m.reply(f"`{word}` blacklisted !")

Client.on_message(filters.command(["rmblacklist", "rmblocklist"]))
async def rmblacklist(_, m):
    if not m.from_user.id in DEV_USERS:
        x = await _.get_chat_member(m.chat.id, m.from_user.id)
        if not x.status in ["creator", "administrator"]:
            return await m.reply("Only admin can perform this action !")
    if not len(m.command) > 1:
        return await m.reply("`/rmblacklist < word > `")
    word = m.text.split()[1] 
    check = await is_blacklist(m.chat.id, word)
    if not check:
        return await m.reply(f"`{word}` isn't blacklisted !")
    await del_blacklist(m.chat.id, word)
    await m.reply(f"`{word}` removed from blacklist !")
    
