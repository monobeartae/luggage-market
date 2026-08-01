"""
/deletepayment Charlie
"""

from telegram import Update
from telegram.ext import ContextTypes

from models import delete_payment_source


async def delete_payment_source_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    if len(context.args) == 0:

        await update.message.reply_text(
            "Usage:\n/deletepayment NAME"
        )
        return

    name = " ".join(context.args)

    deleted = delete_payment_source(chat_id, name)

    if deleted:

        await update.message.reply_text(
            f"Payment source {name} deleted"
        )

    else:

        await update.message.reply_text(
            f"Payment source {name} not found or has existing sales."
        )
