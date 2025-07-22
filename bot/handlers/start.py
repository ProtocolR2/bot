import os
from telegram import Update
from telegram.ext import ContextTypes

from bot.services.backend_api import check_user_registered, activate_user
from bot.handlers.menu import show_main_menu

# Leer admins desde variable de entorno (ejemplo: "234241,12424")
admin_ids_str = os.getenv("admin_telegram_ids", "")
# Convertir string a lista de ints, filtrando posibles espacios vacíos
ADMINS = {}
for admin_id_str in admin_ids_str.split(","):
    admin_id_str = admin_id_str.strip()
    if admin_id_str.isdigit():
        ADMINS[int(admin_id_str)] = "Hola Amo 👑"  # Mensaje default, puedes luego personalizar por id

# Mensajes personalizados para admins específicos (opcional)
custom_admin_messages = {
    7237906261: "Hola Amo 👑",
    503453442: "Hola Maria 👑, Reina de mi bot ❤️",
    # Puedes agregar más admins y mensajes aquí
}
for admin_id in ADMINS:
    if admin_id in custom_admin_messages:
        ADMINS[admin_id] = custom_admin_messages[admin_id]

# URL de la landing para compra
LANDING_URL = "https://tulandingdepago.com"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.effective_user.id
    args = context.args  # Token si viene con /start <token>

    # 1. Si es admin, acceso directo con saludo personalizado
    if telegram_id in ADMINS:
        await update.message.reply_text(ADMINS[telegram_id])
        await show_main_menu(update, context)
        return

    # 2. Intentar activación si viene token
    if args:
        token = args[0]
        if activate_user(telegram_id, token):
            await update.message.reply_text(
                "🎉 ¡Cuenta activada correctamente!\n\nYa podés acceder a tu menú principal:"
            )
            await show_main_menu(update, context)
            return
        else:
            await update.message.reply_text(
                "❌ Token inválido o ya usado. Si creés que es un error, escribinos."
            )
            return

    # 3. Usuarios normales registrados
    if check_user_registered(telegram_id):
        await update.message.reply_text("👋 ¡Hola de nuevo!")
        await show_main_menu(update, context)
    else:
        # 4. Usuarios no registrados -> mensaje con link a landing
        await update.message.reply_text(
            f"Acceso denegado, este bot es parte del programa pago protocol R2.\n\n"
            f"Completa tu compra para acceder:\n{LANDING_URL}"
        )
