**Habit Tracker**

Habit Tracker - это приложение Django, предназначенное для отслеживания пользовательских привычек. Оно включает интеграцию с Telegram для отправки уведомлений о привычках.

Особенности

Создание, редактирование и удаление привычек.
Просмотр списка всех привычек и публичных привычек.
Интеграция с Telegram для отправки уведомлений о привычках.
Настройка Telegram Бота

Чтобы использовать возможности уведомлений через Telegram, необходимо выполнить следующие шаги:

Создание Бота: Воспользуйтесь BotFather в Telegram для создания нового бота. Получите токен бота и сохраните его.

Настройка токена в проекте: Добавьте полученный токен бота в файл .env вашего проекта как TELEGRAM_BOT_TOKEN.

Запуск бота: Запустите скрипт бота в вашем Django-приложении, чтобы он начал прослушивать команды и отправлять уведомления:

`python telegram_bot.py`

Запустите Django-сервер:

dev-режим: `python manage.py runserver`

Запустите скрипты фоновых задач:

`celery -A habit_tracker worker --loglevel=info`

`celery -A habit_tracker beat --loglevel=info`

Использование Уведомлений

После настройки Telegram бота и запуска вашего Django-приложения пользователи смогут получать уведомления о своих привычках. Уведомления отправляются автоматически при следующих событиях:

Создание привычки: Когда пользователь создает новую привычку, он получает уведомление в Telegram.
Обновление привычки: При изменении существующей привычки пользователь получит соответствующее уведомление.
Удаление привычки: Уведомление об удалении привычки также отправляется пользователю.
Конфигурация

Убедитесь, что ваше приложение и бот настроены правильно:

Проверьте, что токен Telegram бота добавлен в .env.
Запустите миграции Django для создания необходимых таблиц базы данных.
Запустите Celery worker для обработки асинхронных задач уведомлений.