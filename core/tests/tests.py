import pytest
from django.utils import timezone
from rest_framework.test import APIClient
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied
from core.models import User, Token, GameHistory
from core.services.game_service import play_logic

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user():
    return User.objects.create(username="test_user", phone_number="+380991112233")

@pytest.fixture
def token(user):
    return Token.objects.create(user=user)

@pytest.mark.django_db
class TestUserRegistration:

    def test_register_user_success(self, api_client):
        data = {"username": "new_user", "phone_number": "+380991100011"}
        response = api_client.post("/user/register", data)
        assert response.status_code == 201
        resp_data = response.json()
        assert "user_id" in resp_data
        assert "token" in resp_data
        assert "token_expires_at" in resp_data

    def test_register_user_invalid(self, api_client):
        data = {"username": "", "phone_number": "invalid"}
        response = api_client.post("/user/register", data)
        assert response.status_code == 400


@pytest.mark.django_db
class TestTokenValidation:

    def test_get_user_by_token_success(self, api_client, token):
        response = api_client.get(f"/game/{token.id}")
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == token.user.username
        assert data["phone_number"] == token.user.phone_number

    def test_get_user_by_invalid_token(self, api_client):
        response = api_client.get("/game/00000000-0000-0000-0000-000000000000")
        assert response.status_code == 403  # AuthenticationFailed

    def test_get_user_by_expired_token(self, api_client, token):
        token.expires_at = timezone.now() - timezone.timedelta(days=1)
        token.save()
        response = api_client.get(f"/game/{token.id}")
        assert response.status_code == 403  # PermissionDenied


@pytest.mark.django_db
class TestTokenLifecycle:

    def test_renew_token(self, api_client, token):
        old_id = token.id
        response = api_client.post(f"/game/{old_id}/renew")
        assert response.status_code == 200
        data = response.json()
        assert "token" in data
        assert data["token"] != str(old_id)
        token.refresh_from_db()
        assert not token.is_active

    def test_deactivate_token(self, api_client, token):
        response = api_client.post(f"/game/{token.id}/deactivate")
        assert response.status_code == 200
        token.refresh_from_db()
        assert not token.is_active


@pytest.mark.django_db
class TestGamePlay:

    def test_play_game_win_or_lose(self, api_client, token):
        response = api_client.post(f"/game/{token.id}/play")
        assert response.status_code == 200
        data = response.json()
        assert "random_number" in data
        assert "result" in data
        assert data["result"] in ["win", "lose"]
        assert "prize" in data


        number = data["random_number"]
        result = data["result"]
        prize = data["prize"]

        if number % 2 == 0:
            assert result == "win"
            if number > 900:
                assert prize == number * 0.7
            elif number > 600:
                assert prize == number * 0.5
            elif number > 300:
                assert prize == number * 0.3
            else:
                assert prize == number * 0.1
        else:
            assert result == "lose"
            assert prize == 0


@pytest.mark.django_db
class TestGameHistory:

    def test_game_history_limit(self, api_client, token):

        for _ in range(5):
            number, result, prize = play_logic()
            GameHistory.objects.create(
                user=token.user,
                token=token,
                random_number=number,
                result=result,
                prize=prize
            )

        response = api_client.get(f"/game/{token.id}/history")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3
        last_ids = [gh["id"] for gh in data]
        histories = GameHistory.objects.filter(user=token.user).order_by('-created_at')[:3]
        expected_ids = [h.id for h in histories]
        assert last_ids == expected_ids
