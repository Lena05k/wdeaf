
import os
from pathlib import Path
from dotenv import load_dotenv, find_dotenv

# ============================================================================
# ENVIRONMENT LOADING
# ============================================================================

# Метод 1: Используем find_dotenv с usecwd=True
env_file = find_dotenv(usecwd=True)
print(f"🔍 Ищу .env файл в: {os.getcwd()}")
print(f"📁 Найден .env файл: {env_file}")

if env_file:
    load_dotenv(env_file)
    print(f"✅ Загружен .env файл: {env_file}")
else:
    print("⚠️  .env файл не найден! Использую переменные окружения.")

# Метод 2: Если первый способ не сработал, попробуем явный путь
backend_dir = Path(__file__).parent
env_path = backend_dir / '.env'
if env_path.exists():
    load_dotenv(env_path, override=True)
    print(f"✅ Явно загружен: {env_path}")

# ============================================================================
# TELEGRAM BOT CONFIGURATION
# ============================================================================

BOT_TOKEN = os.getenv('BOT_TOKEN')
WEBHOOK_URL = os.getenv('WEBHOOK_URL')
MINI_APP_URL = os.getenv('MINI_APP_URL')
ADMIN_CHAT_ID = os.getenv('ADMIN_CHAT_ID', '0')
PORT = int(os.getenv('PORT', 8000))

# ============================================================================
# VALIDATION AND DEBUG INFO
# ============================================================================

print("\n" + "="*70)
print("🔐 CONFIGURATION VALIDATION")
print("="*70)

if BOT_TOKEN:
    print(f"✅ BOT_TOKEN: {BOT_TOKEN[:20]}...{BOT_TOKEN[-5:]}")
else:
    print("❌ BOT_TOKEN: NOT SET!")

if WEBHOOK_URL:
    print(f"✅ WEBHOOK_URL: {WEBHOOK_URL}")
else:
    print("❌ WEBHOOK_URL: NOT SET!")

if MINI_APP_URL:
    print(f"✅ MINI_APP_URL: {MINI_APP_URL}")
else:
    print("❌ MINI_APP_URL: NOT SET!")

print(f"✅ PORT: {PORT}")
print(f"✅ ADMIN_CHAT_ID: {ADMIN_CHAT_ID}")

print("="*70 + "\n")

if not BOT_TOKEN or BOT_TOKEN.strip() == '':
    raise ValueError(
        "❌ ERROR: BOT_TOKEN is not set!\n"
        "   1. Create backend/.env file\n"
        "   2. Add: BOT_TOKEN=8231118642:AAEPlfNp_21pVnKHxOjECUp_jFiMxEpu3Co\n"
        "   3. Save and restart the application"
    )

if not WEBHOOK_URL or WEBHOOK_URL.strip() == '':
    raise ValueError(
        "❌ ERROR: WEBHOOK_URL is not set!\n"
        "   1. Check backend/.env file\n"
        "   2. Add: WEBHOOK_URL=https://0008c5ee-9c57-4c0c-8c42-95e34f04c764.tunnel4.com\n"
        "   3. Save and restart"
    )

if not MINI_APP_URL or MINI_APP_URL.strip() == '':
    raise ValueError(
        "❌ ERROR: MINI_APP_URL is not set!\n"
        "   1. Check backend/.env file\n"
        "   2. Add: MINI_APP_URL=https://0008c5ee-9c57-4c0c-8c42-95e34f04c764.tunnel4.com\n"
        "   3. Save and restart"
    )

# Convert ADMIN_CHAT_ID to int safely
try:
    ADMIN_CHAT_ID = int(ADMIN_CHAT_ID) if ADMIN_CHAT_ID else 0
except ValueError:
    ADMIN_CHAT_ID = 0

DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///wdeaf.db')

print(f"✅ Database: {DATABASE_URL}\n")
