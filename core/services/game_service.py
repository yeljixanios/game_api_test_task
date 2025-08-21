import random
from core.models import GameHistory

def play_logic() -> tuple[int, str, float]:
    number = random.randint(1, 1000)

    if number % 2 == 0:
        result = 'win'
        prize = calculate_prize(number)
    else:
        result = 'lose'
        prize = 0

    return number, result, prize

def calculate_prize(number: int) -> float:
    if number > 900:
        return number * 0.7
    elif number > 600:
        return number * 0.5
    elif number > 300:
        return number * 0.3
    return number * 0.1

def save_game(user, token, number: int, result: str, prize: float) -> GameHistory:
    return GameHistory.objects.create(
        user=user,
        token=token,
        random_number=number,
        result=result,
        prize=prize
    )
