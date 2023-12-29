# Используем официальный образ Python как базовый образ
FROM python:3.9

# Устанавливаем переменные окружения для Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файл 'requirements.txt' в рабочую директорию
COPY requirements.txt /app/

# Устанавливаем зависимости Python из файла 'requirements.txt'
RUN pip install --no-cache-dir -r requirements.txt

# Копируем содержимое локальной директории в рабочую директорию контейнера
COPY . /app/

# Команда для запуска приложения Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
