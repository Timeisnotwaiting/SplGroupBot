from pyrogram import Client, filters
from config import DEV
from Spoiled.Database.filters import *
from pyrogram.types import InlineKeyboardButton as IKB, InlineKeyboardMarkup as IKM

DEV_USERS = DEV.SUDO_USERS + [DEV.OWNER_ID]

markup = IKM(
         [
         [
         IKB("Clear 🗑️", callback_data="clear_filters")
         ]
         ]
         )

@Client.on_callback_query(filters.regex("clear_filters"))
async def cbq(_, q):
    id = q.from_user.id
    if not id in DEV_USERS:
        x = await _.get_chat_member(q.message.chat.id, id)
        if x.status.name != "OWNER":
            return await q.answer("Only owner can clear all at once !", show_alert=True)
    await q.answer("clearing...")
    await del_all_filters(q.message.chat.id)
    await q.edit_message_text("All filters cleared !")

@Client.on_message(filters.command("filter") & filters.group)
async def filter(_, m):
    id = m.from_user.id
    if not id in DEV_USERS:
        x = await _.get_chat_member(m.chat.id, id)
        if not x.privileges:
            return await m.reply("**You don't have right to do this !**")
        x = x.privileges
        if not x.can_change_info:
            return await m.reply("**You don't have right to edit filters !**")
    reply = m.reply_to_message
    if not reply:
        txt = m.text.split()
        if len(txt) < 3:
            return await m.reply("**/filter trigger text**")
        trigger = m.text.split()[1]
        content = {"file": None, "text": m.text.split(None, 2)[2]}
    if reply:
        if reply.text:
            if len(m.command) < 2:
                return await m.reply("**Give a word to filter it !**")
            trigger = m.text.split()[1]
            content = {"file": None, "text": reply.text}
        elif reply.media:
            caption = reply.caption if reply.caption else None
            if len(m.command) < 2:
                return await m.reply("**Give a word to filter it !**")
            elif reply.photo:
                content = {"file": ["photo", reply.photo.file_id], "text": caption}
            elif reply.video:
                content = {"file": ["video", reply.video.file_id], "text": caption}
            elif reply.sticker:
                content = {"file": ["sticker", reply.sticker.file_id], "text": caption}
            elif reply.document:
                content = {"file": ["document", reply.document.file_id], "text": caption}
            elif reply.audio:
                content = {"file": ["audio", reply.audio.file_id], "text": caption}
            elif reply.voice:
                content = {"file": ["voice", reply.voice.file_id], "text": caption}
            elif reply.animation:
                content = {"file": ["animation", reply.animation.file_id], "text": caption}
            else:
                return
            trigger = m.text.split()[1]
    await add_filter(m.chat.id, [trigger.lower(), content])
    await m.reply(f"**Filter saved ~** `{trigger}`")

@Client.on_message(filters.command("stop") & filters.group)
async def stopper(_, m):
    id = m.from_user.id
    if not id in DEV_USERS:
        x = await _.get_chat_member(m.chat.id, id)
        if not x.privileges:
            return await m.reply("**You don't have right to do this !**")
        x = x.privileges
        if not x.can_change_info:
            return await m.reply("**You don't have right to edit filters !**")
    if len(m.command) < 2:
        return await m.reply("**Give filter name to stop !**")
    filname = m.text.split()[1].lower()
    x = await is_filter(m.chat.id, filname)
    if not x:
        return await m.reply("**No filter saved with this name !**")
    await del_filter(m.chat.id, filname)
    await m.reply(f"**Filter stopped ~** `{filname}`")

@Client.on_message(filters.command("filters") & filters.group)
async def filter_getter(_, m):
    id = m.from_user.id
    if not id in DEV_USERS:
        x = await _.get_chat_member(m.chat.id, id)
        if not x.privileges:
            return await m.reply("**You don't have right to do this !**")
        x = x.privileges
        if not x.can_change_info:
            return await m.reply("**You don't have right to edit filters !**")
    x = await list_filters(m.chat.id)
    if not x:
        return await m.reply(f"**No filters saved in {m.chat.title}**")
    txt = f"**Filters in {m.chat.title}**"
    txt += "\n\n"
    for g in x:
        txt += f"- `{g}`\n"
    await m.reply(txt, reply_markup=markup)

@Client.on_message(filters.group, group=11)
async def cwf(_, m):
    if m.from_user:
        if m.text or m.caption:
            txt = m.text if m.text else m.caption 
            if txt.split()[0].lower() == "/filter":
                return
            x = await list_filters(m.chat.id)
            for h in txt.split():
                h = h.lower()
                if h.lower() in x:
                    j = await get_filter(m.chat.id, h)
                    if not j["file"]:
                        sext = j["text"]
                        return await m.reply(sext)
                    t = j["file"]
                    if t[0] == "photo":
                        return await m.reply_photo(t[1], caption=j["text"] if "text" in j else None)
                    if t[0] == "video":
                        return await m.reply_video(t[1], caption=j["text"] if "text" in j else None)
                    if t[0] == "audio":
                        return await m.reply_audio(t[1], caption=j["text"] if "text" in j else None)
                    if t[0] == "voice":
                        return await m.reply_voice(t[1], caption=j["text"] if "text" in j else None)
                    if t[0] == "document":
                        return await m.reply_document(t[1], caption=j["text"] if "text" in j else None)
                    if t[0] == "animation":
                        return await m.reply_animation(t[1], caption=j["text"] if "text" in j else None)
                    if t[0] == "sticker":
                        return await m.reply_sticker(t[1])
                
    
        
