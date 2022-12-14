import requests
from telegram.constants import ParseMode
from telegram import Update
from telegram.ext import CallbackContext, CommandHandler
from Spoiled import Yashu

CASH_API_KEY = "-xyz"

async def convert(update: Update, context: CallbackContext):
    args = update.effective_message.text.split(" ")

    if len(args) == 4:
        try:
            orig_cur_amount = float(args[1])

        except ValueError:
            await update.effective_message.reply_text("Invalid Amount Of Currency")
            return

        orig_cur = args[2].upper()

        new_cur = args[3].upper()

        request_url = (
            f"https://www.alphavantage.co/query"
            f"?function=CURRENCY_EXCHANGE_RATE"
            f"&from_currency={orig_cur}"
            f"&to_currency={new_cur}"
            f"&apikey={CASH_API_KEY}"
        )
        response = requests.get(request_url).json()
        try:
            current_rate = float(
                response["Realtime Currency Exchange Rate"]["5. Exchange Rate"]
            )
        except KeyError:
            await update.effective_message.reply_text("Currency Not Supported.")
            return
        new_cur_amount = round(orig_cur_amount * current_rate, 5)
        await update.effective_message.reply_text(
            f"{orig_cur_amount} {orig_cur} = {new_cur_amount} {new_cur}"
        )

    elif len(args) == 1:
        await update.effective_message.reply_text(
            "example syntax: /cash 1 USD INR", parse_mode=ParseMode.MARKDOWN
        )

    else:
        await update.effective_message.reply_text(
            f"*Invalid Args!!:* Required 3 But Passed {len(args) -1}",
            parse_mode=ParseMode.MARKDOWN,
        )

Yashu.add_handler(CommandHandler("cash", convert))
