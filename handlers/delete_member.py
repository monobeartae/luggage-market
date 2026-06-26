"""
/deletemember Charlie
"""

from telegram import Update
from telegram.ext import ContextTypes

from models import delete_member


async def delete_member_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    if len(context.args) == 0:

        await update.message.reply_text(
            "Usage:\n/deletemember NAME"
        )
        return

    name = " ".join(context.args)

    deleted = delete_member(chat_id, name)

    if deleted:

        await update.message.reply_text(
            f"Member {name} deleted"
        )

    else:

        await update.message.reply_text(
            f"Member {name} not found or has existing sales."
        )
