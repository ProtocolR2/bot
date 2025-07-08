from bot.handlers import start as start_handler

conv_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start_handler.start)],
    states={
        start_handler.ASK_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, start_handler.ask_email)],
        start_handler.ASK_EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, start_handler.complete_registration)],
    },
    fallbacks=[CommandHandler("cancel", start_handler.cancel_registration)],
)

application.add_handler(conv_handler)
