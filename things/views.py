from django.shortcuts import render, redirect
from django.db.models import F, Sum, Count, Case, When
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from honauth.models import HonStatSettings
from .models import *
from .forms import *


# Create your views here.
def hero_list(request):
    heros = Hero.objects.all()
    return render(request, 'honete/list_heros.html', {'heros': heros})


def hero_detail(request, id_hero):
    hero = Hero.objects.filter(id=id_hero).first()
    players = PlayersGame.objects.values('player__name').annotate(total_kill=Sum('kills'), total_die=Sum('dead'), total_assist=Sum('assitances')).order_by('total_kill')
    return render(request, 'honete/detail_hero.html', {'hero': hero})


@login_required
def hero_add(request):
    if request.method == 'POST':
        form = HeroForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(reverse_lazy('heros_list'))
        else:
            return render(request, 'honete/form_hero.html', {'form': form})
    form = HeroForm()
    return render(request, 'honete/form_hero.html', {'form': form})


@login_required
def hero_del(request):
    for hero in Hero.objects.all():
        hero.delete()
    return  render(request, 'honete/delete_heros.html')


def games_list(request):
    error = ''
    games = Game.objects.all()
    form = GameForm()
    if request.method == 'POST':
        form = GameForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                form.save()
                return render(request, 'honete/list_games.html', {'games': games, 'upload_form': form, 'errors': error})
            except ValidationError as e:
                error = str(e)[0]
                return render(request, 'honete/form_games.html', {'games': games, 'upload_form': form, 'errors': error})
    return render(request, 'honete/list_games.html', {'games': games, 'upload_form': form, 'errors': error})


@login_required
def game_add(request):
    error = ''
    mess = 'El log no se ha salvado: puede ser por una de las siguientes razones\n' + \
           '1. El Log era de un juego en el que perticipaban menos de 6 juegadores.\n' + \
           '2. Ya Hay un log con iguales caracteristicas o este mismo log ya se guardó.\n' + \
           '3. El log está incompleto o el juego no fue termindao.\n'
    if request.method == 'POST':
        form = GameForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                game = form.save()
                print(game, 'games_sta')
                if game.id:
                    return redirect(reverse_lazy('games_sta', kwargs={'id_game': game.id}))
                else:

                    messages.error(request, mess)
                    return redirect(reverse_lazy('games_list'))
            except ValidationError as e:
                error = str(e)
                return render(request, 'honete/form_games.html', {'form': form, 'errors': error})
        else:
            return render(request, 'honete/form_games.html', {'form': form, 'errors': error})
    form = GameForm()
    return render(request, 'honete/form_games.html', {'form': form, 'errors': error})


@login_required
def game_delete_all(request):
    for game in Game.objects.all():
        game.delete()
    return render(request, 'honete/delete_games.html')


def stats_game(request, id_game):
    game = Game.objects.filter(id=id_game).first()
    return render(request, 'honete/stats_game.html', {'players': game.playersgame_set.all(), 'game': game})


def player_list(request):
    players = Player.objects.all()
    return render(request, 'honete/list_players.html', {'players': players})


def stats(request):
    players = []
    pr: HonStatSettings = HonStatSettings.objects.first()
    for player in Player.objects.exclude(playersgame__isnull=True):
        pog = PlayersGame.objects.exclude(kills=0, dead=0, assitances=0)\
                                 .filter(player=player)\
                                 .aggregate(games=Count('id'),
                                            kills=Sum('kills'),
                                            deads=Sum('dead'),
                                            experienc=Sum('experiens'),
                                            golds=Sum('golds'),
                                            assists=Sum('assitances'),
                                            damage=Sum('damage'),
                                            first_kills=Sum(Case(When(firstblood=-1, then=0), default=1,
                                                                 output_field=models.IntegerField())),
                                            first_dies=Sum(Case(When(firstblood_die=-1, then=0), default=1,
                                                                output_field=models.IntegerField())),
                                            wins=Count(Case(When(game__team_win=F('team'), then=1))),
                                            )
        if pog['kills'] != None and pog['deads'] != None and pog['assists'] != None and pog['first_kills'] != None and pog['first_dies'] != None:
            avg = (pog['kills'] * pr.kill_value + pog['deads'] * pr.dead_value + pog['assists'] * pr.assist_value +
                   pog['first_kills'] * pr.fkill_value + pog['first_dies'] * pr.fdead_value +
                   pog['wins'] * pr.win_value + (pog['games'] - pog['wins']) * pr.loose_value)
            if pog['games'] < pr.min_games:
                avg /= pr.min_games
            else:
                avg /= pog['games']
            result = {'name': player.name, 'avg': avg}
            pogr = dict(pog, **result)
            players.append(pogr)
    return render(request, 'honete/stats.html', {'players': players})


def stats_tmp(request):
    players = []
    if request.method == 'POST':
        pass
    pr = HonStatSettings.objects.first()
    for player in Player.objects.exclude(playersgame__isnull=True):
        pog = PlayersGame.objects.exclude(kills=0, dead=0, assitances=0)\
                                 .filter(player=player)\
                                 .aggregate(games=Count('id'),
                                            kills=Sum('kills'),
                                            deads=Sum('dead'),
                                            experienc=Sum('experiens'),
                                            golds=Sum('golds'),
                                            assists=Sum('assitances'),
                                            damage=Sum('damage'),
                                            first_kills=Sum(Case(When(firstblood=-1, then=0), default=1,
                                                                 output_field=models.IntegerField())),
                                            first_dies=Sum(Case(When(firstblood_die=-1, then=0), default=1,
                                                                output_field=models.IntegerField())),
                                            wins=Count(Case(When(game__team_win=F('team'), then=1))),
                                            )
        if pog['kills'] != None and pog['deads'] != None and pog['assists'] != None and pog['first_kills'] != None and pog['first_dies'] != None:
            avg = (pog['kills'] * pr.kill_value + pog['deads'] * pr.dead_value + pog['assists'] * pr.assist_value +
                   pog['first_kills'] * pr.fkill_value + pog['first_dies'] * pr.fdead_value +
                   pog['wins'] * pr.win_value + (pog['games'] - pog['wins']) * pr.loose_value)
            if pog['games'] < pr.min_games:
                avg /= pr.min_games
            else:
                avg /= pog['games']
            result = {'name': player.name, 'avg': avg}
            pogr = dict(pog, **result)
            players.append(pogr)
    return render(request, 'honete/stats_tmp.html', {'players': players})


def home_view(request):
    return render(request, 'honete/homehon.html')


def item_list(request):
    items = Item.objects.all()
    return render(request, 'honete/list_items.html', {'items': items})


def item_detail(request, id_item):
    item = Item.objects.get_object_or_404(id=id_item)
    return render(request, 'honete/detail_item.html', {'item': item})
