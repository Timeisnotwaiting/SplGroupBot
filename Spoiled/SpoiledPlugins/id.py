from pyrogram import Client as Crystal, filters
from pyrogram.types import Message as Aila
#
@Crystal.on_message(filters.command(["id"]))
async def id(_, m: Aila):
    if m.reply_to_message:
        f_n = m.reply_to_message.from_user.first_name
        id = m.reply_to_message.from_user.id
        return await m.reply(f"{f_n} has an ID of <code>{id}</code>.")
    elif len(m.command) == 2:
        hehe = m.text.split(None, 1)[1]
        if hehe[0] == "@":
            try:
                id = (await _.get_users(hehe)).id
            except:
                return await m.reply("username given is invalid 🤧")
            return await m.reply(f"{(await _.get_users(id)).first_name} has an ID of <code>{id}</code>")
        else:
            return await m.reply("Try: <code>/id [username]</code>")
    else:
        if m.chat.type == "private":
            return await m.reply(f"your ID is <code>{m.from_user.id}</code>")
        else:
            return await m.reply(f"user {m.from_user.first_name} has an ID of <code>{m.from_user.id}</code>, chat has an ID <code>{m.chat.id}</code>.")
