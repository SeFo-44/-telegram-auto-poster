from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

from config import (
    BOT_TOKEN,
    OWNER_ID,
)

from database import Database

db = Database()

waiting_for_post = {}
# =========================
# START
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != OWNER_ID:
        return

    text = (
        "أهلاً بك 🌹\n\n"
        "الأوامر:\n\n"
        "/add\n"
        "/list\n"
        "/delete\n"
        "/setinterval\n"
        "/help"
    )

    await update.message.reply_text(text)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await start(update, context)
