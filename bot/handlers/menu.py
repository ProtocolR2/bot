from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📖 Qué es el Protocolo R2", callback_data="info")],
        [InlineKeyboardButton("🥗 Mi receta de hoy", callback_data="receta")],
        [InlineKeyboardButton("🍳 Desayuno", callback_data="desayuno"),
         InlineKeyboardButton("🍲 Almuerzo", callback_data="almuerzo"),
         InlineKeyboardButton("🍜 Cena", callback_data="cena")],
        [InlineKeyboardButton("📚 Recetario Completo", callback_data="recetario")],
        [InlineKeyboardButton("📅 Mi agenda personal", callback_data="agenda")],
        [InlineKeyboardButton("🛒 Lista de compras", callback_data="lista_compras")],
        [InlineKeyboardButton("💡 Tips y ayuda", callback_data="tips")],
        [InlineKeyboardButton("🏆 Mis Logros", callback_data="logros")],
        [InlineKeyboardButton("🤝 Recomendar Programa", callback_data="recomendar")],
        [InlineKeyboardButton("⚙️ Ajustes", callback_data="ajustes")],
    ]

    text = "💬 *Menú Principal del Bot R2*\nElegí una opción:"
    if update.message:
        await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.MARKDOWN)
    elif update.callback_query:
        await update.callback_query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.MARKDOWN)
