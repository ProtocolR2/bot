from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ContextTypes, ConversationHandler

from bot.services.backend_api import check_user_registered, register_user
from bot.handlers.menu import show_main_menu

ASK_NAME, ASK_EMAIL = range(2)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    # Verificar si el usuario está registrado
    if check_user_registered(user_id):
        await update.message.reply_text("✅ ¡Ya estás registrado!")
        await show_main_menu(update, context)
        return ConversationHandler.END

    # Si no está registrado, empezar flujo de registro
    await update.message.reply_text("👋 ¡Bienvenido/a! Para empezar, decime tu nombre:")
    return ASK_NAME

async def ask_email(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.message.text.strip()
    if not name:
        await update.message.reply_text("⚠️ Por favor, ingresá un nombre válido.")
        return ASK_NAME

    context.user_data["name"] = name
    await update.message.reply_text("📧 Ahora decime tu email:")
    return ASK_EMAIL

async def complete_registration(update: Update, context: ContextTypes.DEFAULT_TYPE):
    email = update.message.text.strip()
    name = context.user_data.get("name")
    user = update.effective_user

    user_info = {
        "telegram_id": user.id,
        "first_name": name,
        "username": user.username or "",
        "email": email,
        "language_code": user.language_code or "es",
        "plan": "free",
        "is_verified": False,
    }

    success = register_user(user_info)

    if success:
        await update.message.reply_text("🎉 Registro completado con éxito.")
        await show_main_menu(update, context)
    else:
        await update.message.reply_text("❌ Ocurrió un error al registrar. Por favor, intentá más tarde.")

    return ConversationHandler.END

async def cancel_registration(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Registro cancelado.", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END
