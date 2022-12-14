from pyrogram import Client, filters
from config import DEV
import time

PURGABLE = [DEV.OWNER_ID] + DEV.SUDO_USERS

@Client.on_message(filters.command("purge"))
async def purge(_, m):
    user_id = m.from_user.id
    chat_id = m.chat.id
    me = await _.get_me()
    myid = me.id
    Me = await _.get_chat_member(chat_id, myid)
    Me = Me.privileges
    if not Me.can_delete_messages:
        return await m.reply("I got no rights to purge !")
    await m.delete()
    if not m.reply_to_message:
        return await m.reply("Reply to a message to purge from !")
    is_sudo = True if user_id in PURGABLE else False
    if not is_sudo:
        x = await _.get_chat_member(chat_id, user_id)
        x = x.privileges if x.privileges else None
        if not x:
            return await m.reply("You got no rights to purge !")
        if not x.can_delete_messages:
            return await m.reply("You got no rights to purge !")
        to_id = m.id
        from_id = m.reply_to_message.id
        ids = []
        a = from_id
        alpha = True
        while alpha:
            if a > to_id:
                break
            ids.append(a)
            a += 1
        try:
            await _.delete_messages(chat_id, ids)
            ok = await m.reply("Purged !")
            time.sleep(3)
            await ok.delete()
        except:
            pass
    else:
        to_id = m.id
        from_id = m.reply_to_message.id
        ids = []
        a = from_id
        alpha = True
        while alpha:
            if a > to_id:
                break
            ids.append(a)
            a += 1
        try:
            await _.delete_messages(chat_id, ids)
            ok = await m.reply("Purged !")
            time.sleep(3)
            await ok.delete()
        except:
            pass
        
        
        
