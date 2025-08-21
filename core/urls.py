from django.urls import path
from . import views
from django.urls import re_path


# Using regex to allow both with and without trailing slash for testing.
# On production, we should enforce a single style.
urlpatterns = [
    re_path(r"^user/register/?$", views.register_user, name="register_user"),
    re_path(r"^game/(?P<token>[0-9a-f-]{36})/?$", views.get_user_by_token, name="get_user_by_token"),
    re_path(r"^game/(?P<token>[0-9a-f-]{36})/renew/?$", views.renew_token, name="renew_token"),
    re_path(r"^game/(?P<token>[0-9a-f-]{36})/deactivate/?$", views.deactivate_token, name="deactivate_token"),
    re_path(r"^game/(?P<token>[0-9a-f-]{36})/play/?$", views.play_game, name="play_game"),
    re_path(r"^game/(?P<token>[0-9a-f-]{36})/history/?$", views.game_history, name="game_history"),
]