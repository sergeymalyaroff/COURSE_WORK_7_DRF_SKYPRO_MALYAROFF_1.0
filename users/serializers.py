from rest_framework import serializers


class UsersSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)


class RegisterRequestSerializer(UsersSerializer):
    telegram_chat_id = serializers.CharField(required=True)


class ErrorResponseSerializer(serializers.Serializer):
    error = serializers.CharField()


class SuccessResponseSerializer(serializers.Serializer):
    message = serializers.CharField()
