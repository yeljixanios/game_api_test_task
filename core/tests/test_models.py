import pytest
from django.utils import timezone
from core.models import User, Token, GameHistory

@pytest.fixture
def user():
    return User.objects.create(username="test_user", phone_number="+380991112233")


@pytest.mark.django_db
class TestUserModel:

    def test_create_user(self):
        user = User.objects.create(username="user1", phone_number="+380991112233")
        assert user.id is not None
        assert user.username == "user1"
        assert user.phone_number == "+380991112233"
        assert str(user) == "user1"


@pytest.mark.django_db
class TestTokenModel:

    def test_create_token(self, user):
        token = Token.objects.create(user=user)
        assert token.id is not None
        assert token.user == user
        assert token.is_active is True
        assert token.expires_at > timezone.now()

    def test_token_deactivation(self, user):
        token = Token.objects.create(user=user)
        token.is_active = False
        token.save()
        token.refresh_from_db()
        assert token.is_active is False

    def test_token_str(self, user):
        token = Token.objects.create(user=user)
        assert str(token) == f"{user.username} - {token.id}"


@pytest.mark.django_db
class TestGameHistoryModel:

    def test_create_gamehistory(self, user):
        token = Token.objects.create(user=user)
        game = GameHistory.objects.create(
            user=user,
            token=token,
            random_number=500,
            result="win",
            prize=250.0
        )
        assert game.id is not None
        assert game.user == user
        assert game.token == token
        assert game.random_number == 500
        assert game.result == "win"
        assert game.prize == 250.0

    def test_gamehistory_str(self, user):
        token = Token.objects.create(user=user)
        game = GameHistory.objects.create(
            user=user,
            token=token,
            random_number=400,
            result="lose",
            prize=0
        )
        assert str(game) == f"{game.user.username} - {game.random_number} - {game.result}"
