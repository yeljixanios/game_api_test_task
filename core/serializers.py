from rest_framework import serializers
from .models import User, Token, GameHistory
from django.utils import timezone
import uuid

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'phone_number']

class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ['id', 'user', 'created_at', 'expires_at', 'is_active']
        read_only_fields = ['id', 'created_at', 'expires_at', 'is_active']

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'phone_number']

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        token = Token.objects.create(user=user)
        user.token = token
        return user

class GameHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = GameHistory
        fields = ['id', 'user', 'token', 'random_number', 'result', 'prize', 'created_at']