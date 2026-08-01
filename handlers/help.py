"""
/help command.
"""

from telegram import Update
from telegram.ext import ContextTypes

import textwrap


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(textwrap.dedent(
        """
        Available Commands
        ━━━━━━━━━━━━━━
        📦 Utility
        ━━━━━━━━━━━━━━
        • /help → view this help message

        ━━━━━━━━━━━━━━
        📦 Sales
        ━━━━━━━━━━━━━━
        • /sale PRICE → create a sale
        <i>i.e. /sale 12 → creates a sale of $12</i>
        • /clearsales (optional) DATE → clear sales records
        • /deletesale SALE_NO → delete a specific sale


        ━━━━━━━━━━━━━━
        👥 Payees
        ━━━━━━━━━━━━━━
        • /addpayment NAME → add a payment source
        <i>i.e. /addpayment CASH → adds a payment source named CASH</i>
        • /deletepayment NAME → delete a payment source
        <i>i.e. /deletepayment CASH → deletes the payment source named CASH</i>

        ━━━━━━━━━━━━━━
        👥 Members
        ━━━━━━━━━━━━━━
        • /addmember NAME → add a member
        <i>i.e. /addmember Charlie → adds a member named Charlie</i>
        • /deletemember NAME → delete a member
        <i>i.e. /deletemember Charlie → deletes the member named Charlie</i>
        • /members → view all members

        ━━━━━━━━━━━━━━
        📊 Reports
        ━━━━━━━━━━━━━━
        • /summary → view settlements
        """
    ), parse_mode="HTML")
