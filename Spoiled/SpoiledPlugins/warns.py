from Spoiled.Database.warn import *
from pyrogram import Client, filters
from .admins import sender_admin, is_admin
from . import get_id

@Client.on_message(filters.command(["dwarn"]))
async def dwarn_act(_, m):
    x = await sender_admin(_, m)
    if not x:
        return
    try:
        id = await get_id(_, m)
    except:
        return
    x = is_admin(m.chat.id, id)
    if x:
        return await m.reply("Lol, can't dwarn an admin !")
    await dwarn_user(m.chat.id, id)
    x = await get_warns(m.chat.id, id)
    men = (await _.get_users(id)).mention
    await m.reply(f"{men}, your warnings reduced to {x} {"times" if x > 1 else "time"}")

@Client.on_message(filters.command(["warn"]))
async def warn_act(_, m):
    x = await sender_admin(_, m)
    if not x:
        return
    try:
        id = await get_id(_, m)
    except:
        return
    x = is_admin(m.chat.id, id)
    if x:
        return await m.reply("Lol, can't warn an admin !")
    await warn_user(m.chat.id, id)
    x = await get_warns(m.chat.id, id)
    men = (await _.get_users(id)).mention
    await m.reply(f"{men} be careful..!, You got warned {x} {"times" if x > 1 else "time"}")
