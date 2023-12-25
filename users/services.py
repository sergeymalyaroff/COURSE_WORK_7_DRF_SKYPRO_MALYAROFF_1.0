# COURSE_WORK_&_DRF_SKYPRO_MALYAROFF/habit_tracker/users/services.py

from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

from .models import UserProfile


def create_user_with_profile(username, password, telegram_chat_id=None):
    # Create the User instance
    user = User.objects.create_user(username=username, password=password)

    # Create the UserProfile instance
    UserProfile.objects.create(user=user, telegram_chat_id=str(telegram_chat_id))

    return user


def csrf_exempt_api_view(http_method_names):
    """
    A decorator to make a DRF function-based view exempt from CSRF checks.
    """

    def decorator(view_func):
        # Apply the csrf_exempt decorator first
        view_func = csrf_exempt(view_func)
        # Then apply the api_view decorator
        view_func = api_view(http_method_names)(view_func)
        return view_func

    return decorator
