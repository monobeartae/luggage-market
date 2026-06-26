"""
/summary
"""

from telegram import Update
from telegram.ext import ContextTypes

import models
import settlement


async def summary(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    (items, revenue, received, transfers) = settlement.build_summary(
        models.get_members(chat_id),
        models.get_sales(chat_id),
        models.get_all_sale_items(chat_id)
    )

    if sum(revenue.values()) != sum(received.values()): # TODO: log exception in settlement.py
        await update.message.reply_text(
            "⚠️ Revenue and received amounts do not match. Please check your sales."
        )
        return

    await update.message.reply_text(build_summary(chat_id, items, revenue, received, transfers))

def build_summary(chat_id, items: dict, revenue: dict, received: dict, transfers: list[dict]) -> str:
    text = "Summary\n\n"

    text += f"Total Items Sold: {sum(items.values())}\n"
    text += f"Total Revenue: ${sum(revenue.values()):.2f}\n"

    text += "\nMember Summary:\n"
    for mem in models.get_members(chat_id):
        if mem["name"] in items.keys():
            text += f"• {mem['name']}: ${revenue[mem['name']]:.2f} ({items[mem['name']]} items)\n"

    text += "\nSettlement Breakdown:\n"
    for transfer in transfers:
        text += f"• {transfer['from']} -> {transfer['to']}: ${transfer['amount']:.2f}\n"

    return text
