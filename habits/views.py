# COURSE_WORK_&_DRF_SKYPRO_MALYAROFF/habit_tracker/habits/views.py
import json

from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.models import UserProfile
from .models import Habit
from .serializers import HabitSerializer
from .tasks import send_habit_notification


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_habit(request):
    """
    Создание новой привычки.
    Получает данные из POST-запроса и создает новую привычку для пользователя.
    """
    user = User.objects.get(username=request.user.username)

    data = json.loads(request.body)
    action = data.get("action")
    time = data.get("time")
    place = data.get("place")
    is_nice_habit = data.get("is_nice_habit")
    is_public = data.get("is_public")
    related_habit_id = data.get("related_habit_id")
    reward = data.get("reward")
    frequency = data.get("frequency")
    time_required = data.get("time_required")

    habit = Habit.objects.create(
        user=user,
        action=action,
        time=time,
        place=place,
        is_nice_habit=is_nice_habit,
        is_public=is_public,
        related_habit_id=related_habit_id,
        reward=reward,
        frequency=frequency,
        time_required=time_required,
    )

    if time and frequency:
        schedule, created = IntervalSchedule.objects.get_or_create(
            every=frequency,
            period=IntervalSchedule.DAYS,
        )
        message = f"Пора выполнить действие: {action}"
        PeriodicTask.objects.create(
            interval=schedule,
            name=f"Habit {habit.id}",  # Name of the task
            task='notify',  # Task to execute
            args=json.dumps([str(user.profile.telegram_chat_id), message]),  # Arguments for the task
        )

    if user.profile.telegram_chat_id:
        send_habit_notification.delay(user.profile.telegram_chat_id, f"Создана новая привычка: {action}")

    return JsonResponse({'message': 'Habit created', 'habit_id': habit.id})


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def edit_habit(request, habit_id):
    """
    Редактирование существующей привычки.
    Обновляет данные привычки, если пользователь имеет к ней доступ.
    """
    habit = get_object_or_404(Habit, id=habit_id)
    if habit.user != request.user:
        return JsonResponse({'error': 'You do not have permission'}, status=status.HTTP_403_FORBIDDEN)
    user_profile = UserProfile.objects.get(user=request.user)

    data = request.POST
    habit.action = data.get("action", habit.action)
    habit.time = data.get("time", habit.time)
    habit.place = data.get("place", habit.place)
    habit.is_nice_habit = data.get("is_nice_habit", habit.is_nice_habit)
    habit.is_public = data.get("is_public", habit.is_public)
    habit.related_habit_id = data.get("related_habit_id", habit.related_habit_id)
    habit.reward = data.get("reward", habit.reward)
    habit.frequency = data.get("frequency", habit.frequency)
    habit.time_required = data.get("time_required", habit.time_required)
    habit.save()

    periodic_tasks = PeriodicTask.objects.filter(name=f"Habit {habit.id}")
    for periodic_task in periodic_tasks:
        periodic_task.delete()

    if habit.time and habit.frequency:
        schedule, created = IntervalSchedule.objects.get_or_create(
            every=habit.frequency,
            period=IntervalSchedule.DAYS,
        )
        message = f"Пора выполнить действие: {habit.action}"
        PeriodicTask.objects.create(
            interval=schedule,
            name=f"Habit {habit.id}",  # Name of the task
            task='notify',  # Task to execute
            args=json.dumps([str(user_profile.telegram_chat_id), message]),  # Arguments for the task
        )

    if user_profile.telegram_chat_id:
        send_habit_notification.delay(user_profile.telegram_chat_id, f"Привычка обновлена: {habit.action}")

    return JsonResponse({'message': 'Habit updated successfully'})


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_habit(request, habit_id):
    """
    Удаление привычки.
    Удаляет привычку, если пользователь имеет к ней доступ.
    """
    habit = get_object_or_404(Habit, id=habit_id)
    if habit.user != request.user:
        return JsonResponse({'error': 'You do not have permission'}, status=status.HTTP_403_FORBIDDEN)
    habit.delete()

    periodic_tasks = PeriodicTask.objects.filter(name=f"Habit {habit.id}")
    for periodic_task in periodic_tasks:
        periodic_task.delete()

    user_profile = UserProfile.objects.get(user=request.user)
    if user_profile.telegram_chat_id:
        send_habit_notification.delay(
            user_profile.telegram_chat_id, f"Привычка удалена: {habit.action}")

    return JsonResponse({'message': 'Habit deleted successfully'})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_public_habits(request):
    """
    Получение списка публичных привычек.
    Возвращает список всех публичных привычек для аутентифицированных пользователей.
    """
    habits = Habit.objects.filter(is_public=True)
    serializer = HabitSerializer(habits, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_habits(request):
    """
    Получение списка привычек пользователя.
    Возвращает список привычек, созданных аутентифицированным пользователем, с пагинацией.
    """
    habits = Habit.objects.filter(user=request.user)
    paginator = PageNumberPagination()
    page = paginator.paginate_queryset(habits, request)
    if page is not None:
        serializer = HabitSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)
    serializer = HabitSerializer(habits, many=True)
    return Response(serializer.data)
