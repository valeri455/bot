from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from datetime import time
import random
import os

TOKEN = "7955129896:AAFFELHyZXB2mikm4UTBw3LFRuHoeOW-U14"

IMAGES_FOLDER = "valentine_images"

# Список картинок (должны быть в папке IMAGES_FOLDER)
VALENTINE_IMAGES = [
    "heart1.jpeg",
    "heart2.jpeg",
    "heart3.jpeg",
    "heart4.jpeg",
    "heart5.jpeg",
    "heart6.jpeg",
    "heart7.jpeg"
]
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
    ["🎀 Старт"],  # Основное меню
    ["💌 Валентинка", "🌟 Комплимент"],
    ["💭 Почему я тебя люблю?"]
]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start и кнопки 'Старт'"""
    await update.message.reply_text(
        "Привет! Я бот, который дарит любовь 💖 Выбери:",
        reply_markup=ReplyKeyboardMarkup(KEYBOARD, resize_keyboard=True)
    )

    # Устанавливаем ежедневное "Доброе утро"
    chat_id = update.effective_chat.id
    context.job_queue.run_daily(
        send_morning_message,
        time=time(hour=8, minute=30),
        chat_id=chat_id
    )

async def send_morning_message(context: ContextTypes.DEFAULT_TYPE):
        """Отправляет утреннее сообщение"""
        await context.bot.send_message(
            chat_id=context.job.chat_id,
            text=random.choice(MORNING_MESSAGES)
        )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == "🎀 Старт":
        await start(update, context)
    elif text == "💌 Валентинка":
        # Выбираем случайное изображение
        image_path = os.path.join(IMAGES_FOLDER, random.choice(VALENTINE_IMAGES))

        # Отправляем картинку
        await update.message.reply_photo(
            photo=open(image_path, 'rb'),
            caption="Для тебя с любовью! 💝"
        )
    elif text == "🌟 Комплимент":
        await update.message.reply_text(random.choice(COMPLIMENTS))
    elif text == "💭 Почему я тебя люблю?":
        user_name = update.message.from_user.first_name or "солнышко"
        await update.message.reply_text(
            f"{user_name}, я тебя люблю...\n\n{random.choice(LOVE_REASONS)}"
        )

def main():
    # Проверяем наличие папки с изображениями
    if not os.path.exists(IMAGES_FOLDER):
        os.makedirs(IMAGES_FOLDER)
        print(f"Создана папка {IMAGES_FOLDER}. Добавьте туда изображения!")
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Бот запущен! 🚀")
    app.run_polling()

if __name__ == "__main__":
    main()