from telegram import Update
from telegram.ext import ContextTypes

from bot.services.backend_api import check_user_registered, activate_user
from bot.handlers.menu import show_main_menu

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    /start → Muestra menú (y si viene con token, intenta activación)
    """
    telegram_id = update.effective_user.id
    args = context.args  # token si vino como /start <token>

    # 1. Intentar activación si vino token
    if args:
        token = args[0]
        if activate_user(telegram_id, token):
            await update.message.reply_text(
                "🎉 ¡Cuenta activada correctamente!\n\nYa podés acceder a tu menú principal:"
            )
        else:
            await update.message.reply_text(
                "❌ Token inválido o ya usado. Si creés que es un error, escribinos."
            )
            return  # No mostramos menú si falló activación

    else:
        # 2. Saludo general según registro
        if check_user_registered(telegram_id):
            await update.message.reply_text("👋 ¡Hola de nuevo!")
        else:
            await update.message.reply_text(
                "👋 ¡Bienvenido a Protocol R2!\n\nCuando completes tu compra recibirás un token para activar tu cuenta."
            )

    # 3. Mostrar menú
    await show_main_menu(update, context)
