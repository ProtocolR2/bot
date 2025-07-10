import logging
from telegram.ext import (
    Application,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)
from bot.config import Config
from bot.handlers import start as start_handler
from bot.handlers import menu  # para show_main_menu (si lo necesitás en main)

# Configurar logging para debug
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

def main():
    if not Config.is_valid():
        print("❌ Error: faltan variables de entorno obligatorias (TELEGRAM_TOKEN y/o BACKEND_URL).")
        return

    # Crear la aplicación Telegram
    application = Application.builder().token(Config.BOT_TOKEN).build()

    # Definir ConversationHandler para /start y registro
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

    # Agregar handlers a la aplicación
    application.add_handler(conv_handler)

    # Opcional: agregar handler para mostrar menú fuera del registro
    # application.add_handler(CommandHandler("menu", menu.show_main_menu))

    # Ejecutar el bot con polling (para Render o pruebas locales)
    print("✅ Bot iniciado, esperando mensajes...")
    application.run_polling()

if __name__ == "__main__":
    main()
