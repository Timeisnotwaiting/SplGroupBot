from . import db

filtersdb = db.filters

async def add_filter(chat_id: int, data):
    await filterdb.update_one({"chat_id": chat_id}, {"$set": {"data": data}}, upsert=True)

async def is_filter(chat_id: int, name):
    x = await filterdb.find_one({"chat_id" chat_id})
    if not x:
        return False
    list = x["data"]
    for c in list:
        if c[0] == name:
            return True
    return False
