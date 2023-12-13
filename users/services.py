# COURSE_WORK_&_DRF_SKYPRO_MALYAROFF/habit_tracker/users/services.py

from django.contrib.auth.models import User
from .models import UserProfile


def create_user_with_profile(username, password, telegram_chat_id=None):
    # Create the User instance
    user = User.objects.create_user(username=username, password=password)

    # Create the UserProfile instance
    UserProfile.objects.create(user=user, telegram_chat_id=str(telegram_chat_id))

    return user
