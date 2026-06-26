"""
Entry point for the Clothes Market Telegram Bot.

Responsibilities:
- Initialise the Telegram application.
- Register all command handlers.
- Start polling.

No business logic should be implemented here.
"""

import logging

from telegram.ext import (
    filters,
    Application,
    CallbackQueryHandler,
    CommandHandler,
    MessageHandler,
)

from config import BOT_TOKEN
from database import initialise_database

from handlers.start import start
from handlers.help import help_command
from handlers.add_member import add_member_command
from handlers.delete_member import delete_member_command
from handlers.list_members import list_members_command
from handlers.sale import open_sale_ui, handle_sale_ui, handle_sale_text
from handlers.summary import summary
from handlers.clear_sales import clear_sales


from commands import get_commands


###############################################################################
# Logging
###############################################################################

logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)


###############################################################################
# Register Handlers
###############################################################################

def register_handlers(app: Application) -> None:
    """
    Registers every command and conversation handler.
    """

    # General commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))

    # Member management
    app.add_handler(CommandHandler("addmember", add_member_command))
    app.add_handler(CommandHandler("deletemember", delete_member_command))
    app.add_handler(CommandHandler("members", list_members_command))

    # Sales
    app.add_handler(CommandHandler("sale", open_sale_ui))
    app.add_handler(CallbackQueryHandler(handle_sale_ui))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_sale_text))
    app.add_handler(CommandHandler("clearsales", clear_sales))


    # Reports
    app.add_handler(CommandHandler("summary", summary))


###############################################################################
# Main
###############################################################################

def main() -> None:
    """
    Application entry point.
    """

    logger.info("Initialising database...")
    initialise_database()

    logger.info("Starting Telegram bot...")

    application = (
        Application.builder()
        .token(BOT_TOKEN)
        .build()
    )

    register_handlers(application)

    application.bot.set_my_commands(get_commands())

    logger.info("Bot is running.")

    application.run_polling(
        allowed_updates="all",
        drop_pending_updates=True,
    )


if __name__ == "__main__":
    main()
