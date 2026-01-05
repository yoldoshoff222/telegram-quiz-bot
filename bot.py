# -*- coding: utf-8 -*-
import os
from telegram.ext import Updater, CommandHandler

TOKEN = os.environ.get("BOT_TOKEN")

def start(update, context):
    update.message.reply_text(
        "Assalomu alaykum!\n\n"
        "/fan1 - 1-fan testlari\n"
        "/fan2 - 2-fan testlari"
    )

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
