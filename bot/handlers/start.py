from telegram import Update
from telegram.ext import ContextTypes
from bot.services.backend_api import check_user_registered, activate_user
from bot.handlers.menu import show_main_menu

# Lista de admins con mensajes personalizados
ADMINS = {
    7237906261: "Hola Amo 👑",
    503453442: "Hola 👑 Maria, reina de mi bot ❤️",  # <-- Editalo a gusto
    # Puedes agregar más admins fácilmente:
    # 8888888888: "Hola Admin 3",
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    /start → Muestra menú (y si viene con token, intenta activación)
    """
    telegram_id = update.effective_user.id
    args = context.args  # token si vino como /start <token>

    # 1. Mostrar saludo especial si es admin
    if telegram_id in ADMINS:
        await update.message.reply_text(ADMINS[telegram_id])

    # 2. Intentar activación si vino token
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
        # 3. Verificar si el usuario está registrado (flujo sin token)
        if check_user_registered(telegram_id):
            await update.message.reply_text("👋 ¡Hola de nuevo!")
        else:
            await update.message.reply_text(
                "❌ Acceso denegado.\n\nEste bot es parte del programa pago Protocol R2.\n\n"
                "👉 Completá tu compra para acceder.\n\n"
                # "🔗 Pagá aquí: https://tu-landing.com"  # ← Reemplazá por tu link real
            )
            return  # No mostramos menú si no está registrado

    # 4. Mostrar menú
    await show_main_menu(update, context)
