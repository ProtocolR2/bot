from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Muestra el menú principal del bot."""
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

    if update.message:
        await update.message.reply_text("📋 Menú principal:", reply_markup=InlineKeyboardMarkup(keyboard))
    elif update.callback_query:
        await update.callback_query.edit_message_text("📋 Menú principal:", reply_markup=InlineKeyboardMarkup(keyboard))


async def handle_menu_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Maneja las opciones seleccionadas del menú."""
    query = update.callback_query
    await query.answer()

    data = query.data

    if data == "info":
        await query.edit_message_text(
            "📖 El Protocolo R2 es un programa de 21 días para renovar tu energía y hábitos..."
        )
    elif data == "receta":
        await query.edit_message_text("🥗 Tu receta de hoy estará disponible pronto.")
    elif data == "recetario":
        await query.edit_message_text("📚 Recetario completo... (próximamente)")
    elif data == "agenda":
        await query.edit_message_text("📅 Agenda personal... (próximamente)")
    elif data == "lista_compras":
        await query.edit_message_text("🛒 Lista de compras... (próximamente)")
    elif data == "tips":
        await query.edit_message_text("💡 Tips y ayuda... (próximamente)")
    elif data == "logros":
        await query.edit_message_text("🏆 Logros... (próximamente)")
    elif data == "recomendar":
        await query.edit_message_text("🤝 Compartí este programa con alguien que lo necesite 🙌")
    elif data == "ajustes":
        await query.edit_message_text("⚙️ Próximamente podrás ajustar tus recordatorios y preferencias.")
    elif data in ["desayuno", "almuerzo", "cena"]:
        await query.edit_message_text(f"🍽 Receta para {data}... (próximamente)")
    else:
        await query.edit_message_text("❓ Opción no reconocida.")
