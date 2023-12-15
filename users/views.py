# COURSE_WORK_&_DRF_SKYPRO_MALYAROFF/habit_tracker/users/views.py

import json

from django.contrib.auth import login as login_method, authenticate
from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view

from .services import create_user_with_profile


@api_view(["POST"])
def register(request):
    """
    Регистрация нового пользователя.
    Парсит данные из JSON-запроса и создает нового пользователя.
    """
    data = json.loads(request.body)
    username = data.get("username")
    password = data.get("password")
    telegram_chat_id = data.get("telegram_chat_id")

    if not username or not password or not telegram_chat_id:
        return JsonResponse(
            {'error': 'Parameters: username, password, telegram_chat_id are required'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if User.objects.filter(username=username).exists():
        return JsonResponse({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

    print('a')
    user = create_user_with_profile(username=username, password=password, telegram_chat_id=telegram_chat_id)
    if user is not None:
        login_method(request, user)
        return JsonResponse({'message': 'Registration successful'})
    else:
        return JsonResponse({'error': 'Registration failed'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
def login(request):

    """
    Авторизация пользователя.
    Парсит данные из JSON-запроса и авторизует пользователя.
    """
    data = json.loads(request.body)
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return JsonResponse({'error': 'Both username and password required'})
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login_method(request, user)
        return JsonResponse({'message': 'Login successful'})
    else:
        return JsonResponse({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
