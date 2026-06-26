"""
/start command.
"""

from telegram import Update
from telegram.ext import ContextTypes


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Welcome message.
    """

    await update.message.reply_text(
        "Welcome to Luggage Market Bot!\n"
        "Type /help to view available commands."
    )
