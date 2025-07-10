# bot/bot/main.py

import logging
from fastapi import FastAPI, Request
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes

from bot.config import Config
from bot.handlers import start as start_handler
from bot.handlers import menu  # si usás menú fuera del registro
from telegram.ext import (
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)

# Configurar logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# Inicializar FastAPI
app = FastAPI()

# Inicializar Telegram Application
application = ApplicationBuilder().token(Config.BOT_TOKEN).build()

# Definir handlers (como antes)
conv_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start_handler.start)],
    states={
        start_handler.ASK_NAME: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, start_handler.ask_email)
        ],
        start_handler.ASK_EMAIL: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, start_handler.complete_registration)
        ],
    },
    fallbacks=[CommandHandler("cancel", start_handler.cancel_registration)],
)
application.add_handler(conv_handler)

# Opcional: comando /menu global
# application.add_handler(CommandHandler("menu", menu.show_main_menu))

# Endpoint simple para pruebas
@app.get("/ping")
async def ping():
    return {"status": "ok"}

# Endpoint del webhook
@app.post("/webhook")
async def telegram_webhook(req: Request):
    data = await req.json()
    update = Update.de_json(data, application.bot)
    await application.process_update(update)
    return {"status": "ok"}
