# COURSE_WORK_&_DRF_SKYPRO_MALYAROFF/habit_tracker/habits/telegram_bot.py
from os import getenv

from telegram.ext import CommandHandler, ApplicationBuilder


async def start(update, context):
    """
    Обработчик команды /start.
    Вызывается, когда пользователь отправляет команду /start.
    Отправляет приветственное сообщение пользователю.
    """
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Привет! Я ваш бот для отслеживания привычек.",
    )


async def help_command(update, context):
    """
    Обработчик команды /help.
    Вызывается, когда пользователь отправляет команду /help.
    Отправляет пользователю информацию о том, как использовать бота.
    """
    await update.message.reply_text("Используйте /start для начала работы с ботом.")


def main():
    """
    Основная функция для запуска бота.
    Создает экземпляр Updater и добавляет обработчики команд.
    """
    application = ApplicationBuilder().token(getenv('TELEGRAM_BOT_TOKEN')).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('help', help_command))

    application.run_polling()


if __name__ == "__main__":
    main()
