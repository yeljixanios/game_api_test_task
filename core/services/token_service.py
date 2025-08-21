from django.utils import timezone
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied
from core.models import Token


def validate_token(token_id: str, check_expiry=True) -> Token:
    try:
        token = Token.objects.get(id=token_id, is_active=True)
    except Token.DoesNotExist:
        raise AuthenticationFailed(detail="Invalid or deactivated token")

    if check_expiry and token.expires_at < timezone.now():
        raise PermissionDenied(detail="Token expired")

    return token
