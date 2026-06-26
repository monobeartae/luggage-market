"""
/addmember MEMBER_NAME
"""

from telegram import Update
from telegram.ext import ContextTypes

from models import add_member, get_members


async def add_member_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    if len(context.args) == 0:
        await update.message.reply_text(
            "Usage:\n/addmember NAME"
        )
        return

    name = " ".join(context.args)

    members = get_members(chat_id) # TODO: introduce service layer
    if name in members:
        await update.message.reply_text(
            f"❌ Member already exists: {name}"
        )
        return

    ok = add_member(chat_id, name)

    if not ok:
        await update.message.reply_text(
            f"❌ Failed to add member: {name}"
        )
        return

    await update.message.reply_text(
        f"✅ Added member: {name}"
    )
