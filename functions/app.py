import logging
from http import HTTPStatus
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, Response
from fastapi.middleware.cors import CORSMiddleware

from telegram import Update, BotCommand
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
)

from config import BOT_TOKEN, WEBHOOK_URL, ALLOWED_ORIGINS
from handlers import WdeafHandlers, setup_menu_button
from auth import router as auth_router
from database import init_db, close_db

# ============================================================================
# LOGGING
# ============================================================================

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger("wdeaf")

# ============================================================================
# TELEGRAM BOT
# ============================================================================

ptb = Application.builder().token(BOT_TOKEN).build()

ptb.add_handler(CommandHandler("start", WdeafHandlers.start_command))
ptb.add_handler(CommandHandler("help", WdeafHandlers.help_command))
ptb.add_handler(CommandHandler("profile", WdeafHandlers.profile_command))
ptb.add_handler(CommandHandler("settings", WdeafHandlers.settings_command))
ptb.add_handler(
    MessageHandler(
        filters.StatusUpdate.WEB_APP_DATA,
        WdeafHandlers.handle_web_app_data,
    )
)
ptb.add_handler(CallbackQueryHandler(WdeafHandlers.button_callback))

# ============================================================================
# BOT COMMANDS
# ============================================================================

async def setup_bot_commands():
    commands = [
        BotCommand("start", "Главное меню и Mini App"),
        BotCommand("profile", "Профиль"),
        BotCommand("settings", "Настройки"),
        BotCommand("help", "Справка"),
    ]
    await ptb.bot.set_my_commands(commands)
    logger.info("✅ Bot commands set")

# ============================================================================
# FASTAPI LIFESPAN
# ============================================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    # -------- startup --------
    logger.info("🚀 Starting bot...")

    # Database
    await init_db()
    logger.info("✅ Database initialized")

    # Bot
    await ptb.initialize()
    await setup_bot_commands()
    await setup_menu_button(ptb.bot)
    await ptb.start()

    logger.info("✅ Bot started")

    yield  # ← приложение работает

    # -------- shutdown --------
    logger.info("🛑 Stopping bot...")

    await ptb.stop()
    await ptb.shutdown()
    await close_db()

    logger.info("✅ Bot stopped")

# ============================================================================
# FASTAPI APP
# ============================================================================

app = FastAPI(
    title="WDEAF Telegram Bot",
    version="1.0.0",
    lifespan=lifespan,
)

# ============================================================================
# CORS MIDDLEWARE
# ============================================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger.info(f"✅ CORS configured for origins: {ALLOWED_ORIGINS}")

# ============================================================================
# INCLUDE ROUTERS
# ============================================================================

app.include_router(auth_router)

# ============================================================================
# ROUTES
# ============================================================================

@app.post("/telegram")
async def telegram_webhook(request: Request):
    try:
        data = await request.json()
        update = Update.de_json(data, ptb.bot)
        await ptb.process_update(update)
        return Response(status_code=HTTPStatus.OK)
    except Exception:
        logger.exception("Webhook error")
        return Response(status_code=HTTPStatus.INTERNAL_SERVER_ERROR)


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "service": "WDEAF",
    }


@app.post("/set-webhook")
async def set_webhook():
    try:
        url = f"{WEBHOOK_URL.rstrip('/')}/telegram"
        await ptb.bot.set_webhook(
            url=url,
            allowed_updates=Update.ALL_TYPES,
        )
        return {"success": True, "webhook": url}
    except Exception:
        logger.exception("Set webhook error")
        return JSONResponse(
            status_code=500,
            content={"error": "Failed to set webhook"},
        )


@app.post("/delete-webhook")
async def delete_webhook():
    try:
        await ptb.bot.delete_webhook()
        return {"success": True}
    except Exception:
        logger.exception("Delete webhook error")
        return JSONResponse(
            status_code=500,
            content={"error": "Failed to delete webhook"},
        )


@app.get("/webhook-info")
async def webhook_info():
    try:
        info = await ptb.bot.get_webhook_info()
        return {
            "url": info.url,
            "pending": info.pending_update_count,
            "last_error": info.last_error_message,
        }
    except Exception:
        logger.exception("Webhook info error")
        return JSONResponse(
            status_code=500,
            content={"error": "Failed to get webhook info"},
        )


@app.get("/api/bot-info")
async def bot_info():
    me = await ptb.bot.get_me()
    return {
        "id": me.id,
        "username": me.username,
        "first_name": me.first_name,
        "is_bot": me.is_bot,
    }
