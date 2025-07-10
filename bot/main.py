import os
import asyncio
import logging

from fastapi import FastAPI
from telegram.ext import (
    Application,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)
from bot.config import Config
from bot.handlers import start as start_handler
from bot.handlers import menu  # si necesitas mostrar menú fuera del registro

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

app = FastAPI()

@app.get("/ping")
async def ping():
    return {"status": "ok"}

async def run_bot():
    if not Config.is_valid():
        print("❌ Error: faltan variables de entorno obligatorias (TELEGRAM_TOKEN y/o BACKEND_URL).")
        return

    application = Application.builder().token(Config.BOT_TOKEN).build()

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

    # Opcional: para menú global
    # application.add_handler(CommandHandler("menu", menu.show_main_menu))

    print("✅ Bot iniciado, esperando mensajes...")
    await application.run_polling()

async def main():
    from uvicorn import Config as UvicornConfig, Server

    port = int(os.getenv("PORT", "8000"))
    config = UvicornConfig(app, host="0.0.0.0", port=port, log_level="info")
    server = Server(config)

    await asyncio.gather(
        server.serve(),
        run_bot()
    )

if __name__ == "__main__":
    asyncio.run(main())
