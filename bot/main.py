# bot/bot/main.py

import logging
from fastapi import FastAPI, Request
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, ConversationHandler, MessageHandler, filters, CallbackQueryHandler

from bot.config import Config
from bot.handlers import start as start_handler
from bot.handlers import menu  # si usás menú fuera del registro

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

# Agregar handler para menú
application.add_handler(CommandHandler("menu", menu.show_main_menu))
application.add_handler(CallbackQueryHandler(menu.handle_menu_selection))

# Endpoint simple para pruebas
@app.get("/ping")
async def ping():
    return {"status": "ok"}

# Endpoint del webhook con logging y manejo de errores
@app.post("/webhook")
async def telegram_webhook(req: Request):
    try:
        data = await req.json()
        logging.info(f"Webhook received data: {data}")
        update = Update.de_json(data, application.bot)
        await application.process_update(update)
        return {"status": "ok"}
    except Exception as e:
        logging.error(f"Error processing update: {e}", exc_info=True)
        return {"status": "error", "detail": str(e)}
