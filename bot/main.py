# bot/bot/main.py

import logging
from fastapi import FastAPI, Request
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
)

from bot.config import Config
from bot.handlers import start as start_handler
from bot.handlers import menu

# Configurar logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# Inicializar FastAPI
app = FastAPI()

# Inicializar Telegram Application
application = ApplicationBuilder().token(Config.BOT_TOKEN).build()

# ✅ Handler principal /start con lógica de activación
application.add_handler(CommandHandler("start", start_handler.start))

# ✅ Handler para mostrar menú manualmente (opcional)
application.add_handler(CommandHandler("menu", menu.show_main_menu))
application.add_handler(CallbackQueryHandler(menu.handle_menu_selection))

# Eventos de arranque y cierre
@app.on_event("startup")
async def on_startup():
    await application.initialize()

@app.on_event("shutdown")
async def on_shutdown():
    await application.shutdown()

# Endpoint de test para ping externo (cron-job.org)
@app.get("/ping")
async def ping():
    return {"status": "ok"}

# Endpoint del webhook
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
