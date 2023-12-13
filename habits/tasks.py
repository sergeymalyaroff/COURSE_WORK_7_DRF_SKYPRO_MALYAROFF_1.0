# habits.tasks.py
from os import getenv
from time import sleep

from celery import shared_task
from requests import get


@shared_task(name='notify')
def send_habit_notification(chat_id, message):
    """
    Отправляет уведомление о привычке пользователю.
    :param bot: Экземпляр бота.
    :param chat_id: ID чата пользователя.
    :param message: Сообщение для отправки.
    """
    url = f"https://api.telegram.org/bot{getenv('TELEGRAM_BOT_TOKEN')}/sendMessage"
    params = {
        'chat_id': str(chat_id),
        'text': message,
    }
    for i in range(10):
        r = get(url, params=params)
        if r.status_code <= 400:
            return
        else:
            sleep(0.2)
    raise Exception(f"'Couldn't send a telegram message to user {chat_id}'")
