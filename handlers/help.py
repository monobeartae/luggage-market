"""
/help command.
"""

from telegram import Update
from telegram.ext import ContextTypes


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        """
        Available Commands

        /start
        /help

        /addmember
        /deletemember
        /members

        /sale

        /summary

        /clearsales
        """
    )
