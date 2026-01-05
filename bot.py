import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

TOKEN = os.environ.get("5863926239:AAFMIoGrSOpKxden0UwpPY7S4gRyVb5gD7U")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "✅ BOT ISHLAYAPTI!\n\n"
        "/fan1 - Yer osti konchilik\n"
        "/fan2 - Maxsus fan"
    )

async def fan1(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📘 FAN 1 tanlandi (testlar keyin qo‘shiladi)")

async def fan2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📕 FAN 2 tanlandi (testlar keyin qo‘shiladi)")

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("fan1", fan1))
    app.add_handler(CommandHandler("fan2", fan2))

    print("BOT ISHLAYAPTI")
    app.run_polling()

if __name__ == "__main__":
    main()
