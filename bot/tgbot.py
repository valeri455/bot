from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from datetime import time
import random
import os

# Токен бота (хранится прямо в коде)
TOKEN = "7955129896:AAFFELHyZXB2mikm4UTBw3LFRuHoeOW-U14"  # Замените на реальный токен

# Конфигурация
IMAGES_FOLDER = "valentine_images"
VALENTINE_IMAGES = ["heart1.jpeg", "heart2.jpeg", "heart3.jpeg", "heart4.jpeg", "heart5.jpeg", "heart6.jpeg",
                    "heart7.jpeg"]
COMPLIMENTS = ["Ты сияешь ярче звёзд! ✨",
               "Твоя улыбка делает мир лучше! 😊",
               "Ты — самое красивое, что случалось в моей жизни! 💘",
               "Мое сердце бьется только для тебя! 💖",
               "Люблю тебя больше, чем котят и пушистые носки! 🐾",
               "Ты мой дом 👩‍❤️‍👩",
               "У тебя самая обаятельная улыбка! 😊",
               "Ты умнее, чем ChatGPT! 🤖",
               "С тобой хочется летать! ✨",
               "Ты — мой личный антистресс! 🧘‍♀️"]
LOVE_REASONS = [
    "Потому что ты заставляешь меня смеяться, даже когда у меня плохое настроение 😊",
    "За твои глаза, в которых я тону каждый день 🌊"
]
MORNING_MESSAGES = ["Доброе утро, солнышко! 🌞 Пусть день будет прекрасным!"]

# Клавиатура
KEYBOARD = [
    ["🎀 Старт"],
    ["💌 Валентинка", "🌟 Комплимент"],
    ["💭 Почему я тебя люблю?"]
]


async def send_morning_message(context: ContextTypes.DEFAULT_TYPE):
    """Отправка утреннего сообщения"""
    await context.bot.send_message(
        chat_id=context.job.chat_id,
        text=random.choice(MORNING_MESSAGES)
    )
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    # Инициализация job_queue если отсутствует
    if not hasattr(context, 'job_queue') or context.job_queue is None:
        context.job_queue = context.application.job_queue

    await update.message.reply_text(
        "Привет! Я бот, который дарит любовь 💖 Выбери:",
        reply_markup=ReplyKeyboardMarkup(KEYBOARD, resize_keyboard=True))

    # Настройка ежедневного сообщения
    context.job_queue.run_daily(send_morning_message,
        time=time(hour=8, minute=30),
        chat_id=update.effective_chat.id
    )

    async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик текстовых сообщений"""
        text = update.message.text
        if text == "🎀 Старт":
            await start(update, context)
        elif text == "💌 Валентинка":
            image_path = os.path.join(IMAGES_FOLDER, random.choice(VALENTINE_IMAGES))
            await update.message.reply_photo(
                photo=open(image_path, 'rb'),
                caption="Для тебя с любовью! 💝")
        elif text == "🌟 Комплимент":
            await update.message.reply_text(random.choice(COMPLIMENTS))
        elif text == "💭 Почему я тебя люблю?":
            name = update.message.from_user.first_name or "солнышко"
            await update.message.reply_text(f"{name}, я тебя люблю...\n\n{random.choice(LOVE_REASONS)}")

    def main():
        """Запуск бота"""
        # Проверка папки с изображениями
        if not os.path.exists(IMAGES_FOLDER):
            os.makedirs(IMAGES_FOLDER)
            print(f"Создана папка {IMAGES_FOLDER}. Добавьте изображения!")

        # Создание и настройка приложения
        app = Application.builder().token(TOKEN).build()

        # Регистрация обработчиков
        app.add_handler(CommandHandler("start", start))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

        print("Бот запущен! 🚀")
        app.run_polling()

    if __name__ == "__main__":
        main()
