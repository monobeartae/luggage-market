from telegram import BotCommand


def get_commands():

    return [

        BotCommand("sale", "Record sale"),

        BotCommand("summary", "View settlement"),

        BotCommand("members", "List members"),

        BotCommand("addmember", "Add member"),
        BotCommand("deletemember", "Delete member"),

        BotCommand("addpayment", "Add payment source"),
        BotCommand("deletepayment", "Delete payment source"),

        BotCommand("clearsales", "Clear sales"),
        BotCommand("deletesale", "Delete sale"),

    ]
