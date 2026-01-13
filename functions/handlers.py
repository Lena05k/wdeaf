from telegram import (
    Update,
    ReplyKeyboardMarkup,
    KeyboardButton,
    MenuButtonWebApp,
    WebAppInfo,
)
from telegram.ext import ContextTypes

from functions.config import MINI_APP_URL


class WdeafHandlers:

    @staticmethod
    async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        keyboard = [
            [KeyboardButton("👤 Профиль"), KeyboardButton("⚙️ Настройки")],
            [KeyboardButton("❓ Помощь")],
        ]

        reply_markup = ReplyKeyboardMarkup(
            keyboard=keyboard,
            resize_keyboard=True,
            one_time_keyboard=False,
        )

        await update.message.reply_text(
            "👋 Бот запущен. Выбери действие:",
            reply_markup=reply_markup,
        )

    @staticmethod
    async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("ℹ️ Помощь")

    @staticmethod
    async def profile_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("👤 Профиль")

    @staticmethod
    async def settings_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("⚙️ Настройки")

    @staticmethod
    async def handle_web_app_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("📦 Получены данные от Mini App")

    @staticmethod
    async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.callback_query.answer("Нажато")


# ============================================================
# MENU BUTTON (ВНЕ КЛАССА!)
# ============================================================

async def setup_menu_button(bot):
    """
    Устанавливает кнопку Mini App рядом со строкой ввода
    """
    await bot.set_chat_menu_button(
        menu_button=MenuButtonWebApp(
            text="Открыть",
            web_app=WebAppInfo(url=MINI_APP_URL),
        )
    )
