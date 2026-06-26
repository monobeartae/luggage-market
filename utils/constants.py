"""
Shared constants for the Telegram bot.
"""

from dataclasses import dataclass


###############################################################################
# Telegram Commands
###############################################################################

@dataclass(frozen=True)
class BotCommandInfo:
    command: str
    name: str
    description: str


START_COMMAND = BotCommandInfo(
    command="start",
    name="Start",
    description="Start the bot"
)

SUMMARY_COMMAND = BotCommandInfo(
    command="summary",
    name="Summary",
    description="View sales breakdown"
)

HELP_COMMAND = BotCommandInfo(
    command="help",
    name="Help",
    description="Show available commands"
)

SALE_COMMAND = BotCommandInfo(
    command="sale",
    name="Sale",
    description="Record a new sale"
)

CLEAR_SALES_COMMAND = BotCommandInfo(
    command="clearsales",
    name="Clear Sales",
    description="Clear sales"
),

RESET_COMMAND = BotCommandInfo(
    command="reset",
    name="Reset",
    description="Reset the bot and wipe all data"
),

LIST_MEMBERS_COMMAND = BotCommandInfo(
    command="members",
    name="List Members",
    description="List members"
)

ADD_MEMBER_COMMAND = BotCommandInfo(
    command="addmember",
    name="Add Member",
    description="Add a member"
)

DELETE_MEMBER_COMMAND = BotCommandInfo(
    command="deletemember",
    name="Delete Member",
    description="Delete a member"
),

COMMANDS = [
    START_COMMAND,
    SUMMARY_COMMAND,
    HELP_COMMAND,
    SALE_COMMAND,
    LIST_MEMBERS_COMMAND,
    ADD_MEMBER_COMMAND,
    DELETE_MEMBER_COMMAND,
    RESET_COMMAND
]


###############################################################################
# Conversation States
###############################################################################

class SaleState:

    SELECT_PAYER = 0

    ENTER_PRICE = 1

    SELECT_ITEMS = 2

    CONFIRM = 3


###############################################################################
# Callback Prefixes
###############################################################################

class Callback:

    PAYER = "payer"

    PLUS = "plus"

    MINUS = "minus"

    SAVE = "save"

    CANCEL = "cancel"
