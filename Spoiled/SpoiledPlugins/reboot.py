from pyrogram import Client, filters
from config import DEV
import os
import time

DEV = DEV.SUDO_USERS + [DEV.OWNER_ID]

@Client.on_message(filters.command("reboot") & filters.user(DEV))
async def reboot(_, m):
    ok = await m.reply("Rebooting, wait for 10sec..")
    time.sleep(3)
    await ok.delete()
    try:
        os.system(f"kill -9 {os.getpid()} && python3 yashu.py")
    except Exception as e:
        await m.reply(e)
