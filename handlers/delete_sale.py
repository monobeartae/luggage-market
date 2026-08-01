"""
/deletesale 5
"""

from models import delete_sale


async def delete_sale_command(update, context):

    chat_id = update.effective_chat.id

    if len(context.args) != 1:
        await update.message.reply_text(
            "Usage: /deletesale <sale number>"
        )
        return

    try:
        sale_no = int(context.args[0])
    except ValueError:
        await update.message.reply_text(
            "Sale number must be an integer."
        )
        return

    if delete_sale(chat_id, sale_no):
        await update.message.reply_text(
            f"✅ Deleted sale #{sale_no}"
        )
    else:
        await update.message.reply_text(
            f"❌ Sale #{sale_no} not found."
        )
