"""
/members
"""

from telegram import Update
from telegram.ext import ContextTypes

from models import get_members


async def list_members_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    members = get_members(chat_id)

    if not members:

        await update.message.reply_text(
            "No members."
        )

        return

    text = "Members\n\n"

    for member in members:

        text += f"• {member['name']}\n"

    await update.message.reply_text(text)
