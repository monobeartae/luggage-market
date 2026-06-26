from telegram import BotCommand


def get_commands():

    return [

        BotCommand("sale", "Record sale"),

        BotCommand("summary", "View settlement"),

        BotCommand("members", "List members"),

        BotCommand("addmember", "Add member"),
        BotCommand("deletemember", "Delete member"),

        BotCommand("clearsales", "Clear sales"),

    ]
