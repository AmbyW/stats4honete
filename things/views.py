from django.shortcuts import render, redirect
from django.db.models import Q, F, Sum, Count, Case, When, Avg
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
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


def hero_del(request):
    for hero in Hero.objects.all():
        hero.delete()
    return  render(request, 'honete/deleted_heros.html')


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


def game_add(request):
    error = ''
    if request.method == 'POST':
        form = GameForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                game = form.save()
                return redirect(reverse_lazy('games_sta', kwargs={'id_game': game.id}))
            except ValidationError as e:
                error = str(e)
                return render(request, 'honete/form_games.html', {'form': form, 'errors': error})
        else:
            return render(request, 'honete/form_games.html', {'form': form, 'errors': error})
    form = GameForm()
    return render(request, 'honete/form_games.html', {'form': form, 'errors': error})


def game_delete_all(request):
    for game in Game.objects.all():
        game.delete()
    return render(request, 'honete/delete_games.html')


def stats_game(request, id_game):
    gameplays = PlayersGame.objects.filter(game_id=id_game)
    game = Game.objects.filter(id=id_game).first()
    return render(request, 'honete/stats_game.html', {'players': gameplays, 'game': game})


def player_list(request):
    players = Player.objects.all()
    return render(request, 'honete/list_players.html', {'players': players})


def stats(request):
    players = []
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
                                            first_kills=Sum(Case(When(firstblood='', then=0), default=1, output_field=models.IntegerField())),
                                            first_dies=Sum(Case(When(firstblood_die='', then=0), default=1, output_field=models.IntegerField())),
                                            wins=Count(Case(When(game__team_win=F('team'), then=1))),
                                            )
        if pog['kills'] != None and pog['deads'] != None and pog['assists'] != None and pog['first_kills'] != None and pog['first_dies'] != None:
            avg = pog['kills'] * 0.5 + pog['deads'] * -0.3 + pog['assists'] * 0.25 + pog['first_kills'] * 0.6 + pog['first_dies'] * -0.5 + pog['wins'] * 0.8 + (pog['games'] - pog['wins']) * -0.4
            if pog['games'] < 20:
                avg /= 20
            else:
                avg /= pog['games']
            pr = {'name': player.name, 'avg': avg}
            pogr = dict(pog, **pr)
            players.append(pogr)
    return render(request, 'honete/stats.html', {'players': players})


def stats_tmp(request):
    players = []
    if request.method == 'POST':
        pass
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
                                            first_kills=Sum(Case(When(firstblood='', then=0), default=1, output_field=models.IntegerField())),
                                            first_dies=Sum(Case(When(firstblood_die='', then=0), default=1, output_field=models.IntegerField())),
                                            wins=Count(Case(When(game__team_win=F('team'), then=1))),
                                            )
        if pog['kills'] != None and pog['deads'] != None and pog['assists'] != None and pog['first_kills'] != None and pog['first_dies'] != None:
            avg = pog['kills'] * 0.5 + pog['deads'] * -0.3 + pog['assists'] * 0.25 + pog['first_kills'] * 0.6 + pog['first_dies'] * -0.2 + pog['wins'] * 0.8 + (pog['games'] - pog['wins']) * -0.2
            if pog['games'] < 20:
                avg /= 20
            else:
                avg /= pog['games']
            pr = {'name': player.name, 'avg': avg}
            pogr = dict(pog, **pr)
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


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        usr = User.objects.filter(username=username).first()
        if usr:
            if usr.is_active:
                account = authenticate(username, password)
                if account:
                    login(request, usr)
                    return redirect(reverse_lazy('home'))
                else:
                    return redirect(reverse_lazy('home'))
            else:
                return redirect(reverse_lazy('home'))
        else:
            return redirect(reverse_lazy('home'))
    return redirect(reverse_lazy('home'))


def logout_view(request):
    logout(request)
    return redirect(reverse_lazy('home'))
