# COURSE_WORK_&_DRF_SKYPRO_MALYAROFF/habit_tracker/users/urls.py

from django.urls import path

from . import views

urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", views.login, name="login"),
]
