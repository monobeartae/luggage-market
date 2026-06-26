"""
/clearsales (optional) DATE
"""

from telegram import Update
from telegram.ext import ContextTypes

from models import clear_all_sales, clear_sales_by_date


async def clear_sales(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    if len(context.args) == 0:
        clear_all_sales(chat_id)
        await update.message.reply_text(
            f"✅ All Sales Records Deleted!"
        )

    else:
        date_string = context.args[0]
        clear_sales_by_date(chat_id, date_string) # TODO: validate date string and change to GUI selection
        await update.message.reply_text(
            f"✅ Sales Records Deleted for {date_string}!"
        )
