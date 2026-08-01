"""
/addpayment PAYMENT_SOURCE_NAME
"""

from telegram import Update
from telegram.ext import ContextTypes

from models import add_payment_source, get_payment_sources


async def add_payment_source_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    if len(context.args) == 0:
        await update.message.reply_text(
            "Usage:\n/addpayment NAME"
        )
        return

    name = " ".join(context.args)

    payment_sources = get_payment_sources(chat_id) # TODO: introduce service layer
    if name in payment_sources:
        await update.message.reply_text(
            f"❌ Payment source already exists: {name}"
        )
        return

    ok = add_payment_source(chat_id, name)

    if not ok:
        await update.message.reply_text(
            f"❌ Failed to add payment source: {name}"
        )
        return

    await update.message.reply_text(
        f"✅ Added payment source: {name}"
    )
