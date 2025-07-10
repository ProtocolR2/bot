from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

MENU_OPTIONS = [
    [InlineKeyboardButton("📖 Qué es el Protocolo R2", callback_data="info")],
    [InlineKeyboardButton("🥗 Mi receta de hoy", callback_data="receta")],
    [
        InlineKeyboardButton("🍳 Desayuno", callback_data="desayuno"),
        InlineKeyboardButton("🍲 Almuerzo", callback_data="almuerzo"),
        InlineKeyboardButton("🍜 Cena", callback_data="cena"),
    ],
    [InlineKeyboardButton("📚 Recetario Completo", callback_data="recetario")],
    [InlineKeyboardButton("📅 Mi agenda personal", callback_data="agenda")],
    [InlineKeyboardButton("🛒 Lista de compras", callback_data="lista_compras")],
    [InlineKeyboardButton("💡 Tips y ayuda", callback_data="tips")],
    [InlineKeyboardButton("🏆 Mis Logros", callback_data="logros")],
    [InlineKeyboardButton("🤝 Recomendar Programa", callback_data="recomendar")],
    [InlineKeyboardButton("⚙️ Ajustes", callback_data="ajustes")],
]

async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Muestra el menú principal del bot."""
    reply_markup = InlineKeyboardMarkup(MENU_OPTIONS)

    if update.message:
        await update.message.reply_text("📋 Menú principal:", reply_markup=reply_markup)
    elif update.callback_query:
        await update.callback_query.edit_message_text("📋 Menú principal:", reply_markup=reply_markup)

async def handle_menu_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Maneja las opciones seleccionadas del menú."""
    query = update.callback_query
    await query.answer()

    responses = {
        "info": "📖 El Protocolo R2 es un programa de 21 días para renovar tu energía y hábitos...",
        "receta": "🥗 Tu receta de hoy estará disponible pronto.",
        "recetario": "📚 Recetario completo... (próximamente)",
        "agenda": "📅 Agenda personal... (próximamente)",
        "lista_compras": "🛒 Lista de compras... (próximamente)",
        "tips": "💡 Tips y ayuda... (próximamente)",
        "logros": "🏆 Logros... (próximamente)",
        "recomendar": "🤝 Compartí este programa con alguien que lo necesite 🙌",
        "ajustes": "⚙️ Próximamente podrás ajustar tus recordatorios y preferencias.",
        "desayuno": "🍽 Receta para desayuno... (próximamente)",
        "almuerzo": "🍽 Receta para almuerzo... (próximamente)",
        "cena": "🍽 Receta para cena... (próximamente)",
    }

    await query.edit_message_text(responses.get(query.data, "❓ Opción no reconocida."))
