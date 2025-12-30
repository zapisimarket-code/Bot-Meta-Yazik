import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from openai import OpenAI

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Получаем ключи из переменных окружения
BOT_TOKEN = os.getenv("8183953049:AAHSnZqbHvu957v52bN7iVVFAzENYeSU3Tw")
DEEPSEEK_API_KEY = os.getenv("sk-f3420576ea824884ae6b344a3f48ece1")

# Проверка ключей
if not BOT_TOKEN:
    print("❌ ОШИБКА: BOT_TOKEN не найден!")
    print("Выполните: export BOT_TOKEN='ваш_токен'")
    exit(1)

if not DEEPSEEK_API_KEY:
    print("❌ ОШИБКА: DEEPSEEK_API_KEY не найден!")
    print("Выполните: export DEEPSEEK_API_KEY='ваш_ключ'")
    exit(1)

# Инициализация клиентов
try:
    client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com")
    app = Application.builder().token(BOT_TOKEN).build()
except Exception as e:
    print(f"❌ Ошибка инициализации: {e}")
    exit(1)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я бот. Используй /ask [вопрос]")

async def ask(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Напиши вопрос после /ask")
        return
    
    question = " ".join(context.args)
    await update.message.reply_text("Думаю...")
    
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": question}],
            max_tokens=500
        )
        
        answer = response.choices[0].message.content
        await update.message.reply_text(answer[:4000])  # Ограничение Telegram
    except Exception as e:
        await update.message.reply_text(f"Ошибка: {str(e)[:100]}")

def main():
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ask", ask))
    
    print("✅ Бот запускается...")
    app.run_polling()

if __name__ == "__main__":
    main()