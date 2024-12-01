import os
import qrcode
from io import BytesIO
from telegram import Update, BotCommand
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

# Функция генерации QR-кода
def generate_qr_code(data: str) -> BytesIO:
    """Генерирует QR-код и возвращает его в виде байтового потока"""
    img = qrcode.make(data)
    byte_io = BytesIO()
    img.save(byte_io, format='PNG')
    byte_io.seek(0)  # Возвращаем указатель на начало потока
    return byte_io

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отправляет сообщение пользователю с инструкцией"""
    await update.message.reply_text(
        "Привет! Отправь мне ссылку, и я сгенерирую QR-код!"
    )

# Команда для генерации QR-кода
async def generate_qr(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Генерирует QR-код из ссылки и отправляет его обратно пользователю"""
    # Получаем текст сообщения (ссылку)
    url = update.message.text

    # Генерация QR-кода
    qr_code_image = generate_qr_code(url)

    # Отправка QR-кода пользователю
    await update.message.reply_photo(photo=qr_code_image)

# Функция для регистрации команд в BotFather
async def post_init(application: Application) -> None:
    bot_commands = [
        BotCommand("start", "Начало работы с ботом"),
        BotCommand("generate_qr", "Генерировать QR-код из ссылки"),
    ]
    await application.bot.set_my_commands(bot_commands)

def main() -> None:
    # создаем приложение 
    application = Application.builder().token("7712924081:AAHQ2pJgijNWAucHVUK4OOpuNAZsLhvYV08").post_init(post_init).build()


    # добавляем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, generate_qr))

    # Запускаем бота
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
