import uuid
from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.core.exceptions import ValidationError
import re

def validate_phone(value):
    # Basic simple test validation of the mobile number, lazy to write full regular (Numbers and +)
    if not re.fullmatch(r"\+?\d{9,20}", value):
        raise ValidationError("Invalid phone number format.")


class User(models.Model):
    username = models.CharField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=20, unique=True, validators=[validate_phone])

    def __str__(self):
        return self.username

def token_expiry():
    return timezone.now() + timedelta(days=7)

class Token(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tokens')
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(default=token_expiry)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} - {self.id}"

class GameHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='game_history')
    token = models.ForeignKey(Token, on_delete=models.SET_NULL,  null=True, blank=True)
    random_number = models.PositiveIntegerField()
    result = models.CharField(max_length=10)
    prize = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.random_number} - {self.result}"