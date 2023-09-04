from django.urls import path
from django.views.generic import RedirectView
from .views import *


urlpatterns = [
    path('games/', games_list, name='games_list'),
    path('games/add/', game_add, name='games_add'),
    path('games/del/', game_delete_all, name='games_del'),
    path('games/stats/<int:id_game>', stats_game, name='games_sta'),
    path('heros/', hero_list, name='heros_list'),
    path('heros/add/', hero_add, name='heros_add'),
    path('heros/del/', hero_del, name='heros_del'),
    path('heros/<int:id_hero>', hero_detail, name='heros_view'),
    path('players/', player_list, name='players_list'),
    path('stats/', stats, name='stats'),
    path('stats/tmp/', stats_tmp, name='stats_tmp'),
    path('items', item_list, name='item_list'),
    path('home/', home_view, name='home'),
    path('', RedirectView.as_view(url=reverse_lazy('home'))),
]
