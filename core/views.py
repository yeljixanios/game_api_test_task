from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils import timezone
from .models import User, Token, GameHistory
from .serializers import UserRegisterSerializer, UserSerializer, TokenSerializer, GameHistorySerializer
import uuid
from core.services.game_service import play_logic, save_game
from core.services.token_service import validate_token


@api_view(['POST'])
def register_user(request):
    serializer = UserRegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token_serializer = TokenSerializer(user.token)
        return Response({
            'user_id': user.id,
            'token': token_serializer.data['id'],
            'token_expires_at': token_serializer.data['expires_at']
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_user_by_token(request, token):
    t = validate_token(token, check_expiry=True)
    serializer = UserSerializer(t.user)
    return Response(serializer.data)

@api_view(['POST'])
def renew_token(request, token):
    old_token = validate_token(token, check_expiry=False)
    old_token.is_active = False
    old_token.save()

    new_token = Token.objects.create(user=old_token.user)
    serializer = TokenSerializer(new_token)
    return Response({
        'token': serializer.data['id'],
        'token_expires_at': serializer.data['expires_at']
    })

@api_view(['POST'])
def deactivate_token(request, token):
    t = validate_token(token, check_expiry=False)

    t.is_active = False
    t.save()
    return Response({'status': 'Token deactivated'})

@api_view(['POST'])
def play_game(request, token):
    t = validate_token(token, check_expiry=True)

    number, result, prize = play_logic()

    save_game(t.user, t, number, result, prize)

    return Response({
        'random_number': number,
        'result': result,
        'prize': prize
    }, status=status.HTTP_200_OK)

@api_view(['GET'])
def game_history(request, token):
    t = validate_token(token, check_expiry=False)
    history = GameHistory.objects.filter(user=t.user)[:3]
    serializer = GameHistorySerializer(history, many=True)
    return Response(serializer.data)