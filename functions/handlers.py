from telegram import Update, MenuButton, MenuButtonWebApp, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes
from config import MINI_APP_URL

class WdeafHandlers:
    @staticmethod
    async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            "🎵 Добро пожаловать в WDEAF!\n\nОткройте приложение через кнопку меню ниже 👇"
        )

async def setup_menu_button(application: Application):
    menu_button = MenuButtonWebApp(
        text="Открыть WDEAF",
        web_app=WebAppInfo(url=MINI_APP_URL)
    )
    await application.bot.set_chat_menu_button(menu_button=menu_button)