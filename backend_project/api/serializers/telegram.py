"""
Telegram authentication serializers
"""
from typing import Any
from rest_framework import serializers


class TelegramAuthRequestSerializer(serializers.Serializer[Any]):
    """
    Telegram WebApp authentication request
    All fields come from Telegram WebApp initData
    """
    id = serializers.IntegerField()
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100, required=False, allow_blank=True)
    username = serializers.CharField(max_length=100, required=False, allow_blank=True)
    photo_url = serializers.URLField(required=False, allow_blank=True)
    auth_date = serializers.IntegerField()
    hash = serializers.CharField()
