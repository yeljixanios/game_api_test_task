import pytest
from rest_framework.test import APIClient
from core.models import Token, User, GameHistory
from django.utils import timezone
from datetime import timedelta
import random

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user():
    return User.objects.create(username="tester", phone_number="+380991122233")

@pytest.fixture
def token(user):
    return Token.objects.create(user=user)

@pytest.mark.django_db
class TestGameAPI:

    def test_expired_token(self, api_client, token):
        token.expires_at = timezone.now() - timedelta(minutes=1)
        token.save()

        response = api_client.post(f"/game/{token.id}/play")
        assert response.status_code == 403

    def test_invalid_token(self, api_client):
        response = api_client.post("/game/999999/play")
        assert response.status_code == 404

    def test_play_logic_boundaries(self, api_client, token, monkeypatch):
        # зробимо генератор, який по черзі видає 300, 600, 900
        values = iter([300, 600, 900])

        def fake_randint(a, b):
            return next(values)

        # підміняємо randint у модулі, де він використовується
        monkeypatch.setattr(random, "randint", fake_randint)

        for number, expected_prize in [(300, 30), (600, 180), (900, 450)]:
            response = api_client.post(
                f"/game/{token.id}/play", {}, format="json"
            )
            assert response.status_code == 200
            data = response.json()
            assert data["result"] == "win"
            assert data["prize"] == expected_prize

    def test_empty_history(self, api_client, user, token):
        response = api_client.get(f"/game/{token.id}/history")
        assert response.status_code == 200
        data = response.json()
        assert data == []
