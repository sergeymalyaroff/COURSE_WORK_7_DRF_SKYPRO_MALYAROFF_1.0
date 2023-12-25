# habits.serialisers.py

# habits/serializers.py

from rest_framework import serializers

from .models import Habit


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = [
            "id",
            "user",
            "place",
            "time",
            "action",
            "is_nice_habit",
            "related_habit",
            "frequency",
            "reward",
            "time_required",
            "is_public",
        ]
        # Добавьте или уберите поля в зависимости от того, какие данные ваша
        # модель содержит и что вы хотите сериализовать


class CreateHabitRequestSerializer(serializers.Serializer):
    action = serializers.CharField(required=True)
    time = serializers.CharField(required=False)
    place = serializers.CharField(required=False)
    is_nice_habit = serializers.BooleanField(required=False)
    is_public = serializers.BooleanField(required=False)
    related_habit_id = serializers.IntegerField(required=False)
    reward = serializers.CharField(required=False)
    frequency = serializers.IntegerField(required=False)
    time_required = serializers.IntegerField(required=False)


class HabitResponseSerializer(serializers.Serializer):
    message = serializers.CharField()
    habit_id = serializers.IntegerField()


class EditHabitRequestSerializer(serializers.Serializer):
    action = serializers.CharField(required=False)
    time = serializers.CharField(required=False)
    place = serializers.CharField(required=False)
    is_nice_habit = serializers.BooleanField(required=False)
    is_public = serializers.BooleanField(required=False)
    related_habit_id = serializers.IntegerField(required=False)
    reward = serializers.CharField(required=False)
    frequency = serializers.IntegerField(required=False)
    time_required = serializers.IntegerField(required=False)


class HabitUpdateResponseSerializer(serializers.Serializer):
    message = serializers.CharField()
