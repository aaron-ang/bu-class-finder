import os
import logging
from datetime import datetime
from pymongo import MongoClient
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = str(os.getenv("TELEGRAM_TOKEN"))
ADMIN_ID = str(os.getenv("CHAT_ID"))
MONGO_URL = str(os.getenv("MONGO_URL"))
GITHUB_URL = "https://github.com/aaron-ang/bu-class-finder"

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
# logger = logging.getLogger(__name__)
client = MongoClient(MONGO_URL)
db = client.course_db


def get_chat_id(update: Update):
    chat = update.effective_chat
    assert chat is not None
    return chat.id


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    now = datetime.now()
    semester = "Fall" if 4 <= now.month < 10 else "Spring"
    year = now.year + 1 if semester == "Spring" else now.year
    chat_id = get_chat_id(update)
    text = f"Welcome to BU Class Finder {semester} {year}! View the source code at {GITHUB_URL}"
    await context.bot.send_message(chat_id=chat_id, text=text)


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = get_chat_id(update)
    await context.bot.send_message(chat_id=chat_id, text="Sorry, I didn't understand that command.")


def main():
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    unknown_handler = MessageHandler(filters.COMMAND, unknown)

    application.add_handler(CommandHandler("start", start))
    application.add_handler(unknown_handler)

    application.run_polling()


if __name__ == "__main__":
    main()
