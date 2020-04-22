from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.db.models import Q, F
from django.core.exceptions import ValidationError, MultipleObjectsReturned
import uuid
from statshon import settings
from things.utils import ParserPlayerGame, ParserGame, parse_data
import datetime
import time
import threading

# Create your models here.
ITEM_CHOISE = (
    {1, 'STARTING'},
    {2, 'MEDIUM'},
    {2, 'END'},
    {2, 'OPTIONALS'},
    {2, 'FULLPOWER'},
)

NUM_WORKERS = 6


def scramble_upload_avatar(instance, filename, subdiretory='avatar_hero'):
    ext = filename.split('.')[-1]
    return subdiretory+'/{}.{}'.format(uuid.uuid4(), ext)


def scramble_upload_log(instance, filename, subdiretory='log_game'):
    ext = filename.split('.')[-1]
    return subdiretory+'/{}.{}'.format(uuid.uuid4(), ext)


def scramble_upload_background(instance, filename, subdiretory='background'):
    ext = filename.split('.')[-1]
    return subdiretory+'/{}.{}'.format(uuid.uuid4(), ext)


def scramble_upload_detail(instance, filename, subdiretory='detail_pic'):
    ext = filename.split('.')[-1]
    return subdiretory+'/{}.{}'.format(uuid.uuid4(), ext)


class TypeTeam(models.Model):
    name = models.CharField(verbose_name=_('Facción'), max_length=25, null=False, blank=False, unique=True)
    code = models.CharField(verbose_name=_('Código'), max_length=1, null=False, blank=False, unique=True)

    class Meta:
        verbose_name = _('Facción')
        verbose_name_plural = _('Facciones')

    def __str__(self):
        return self.name


class TypeHero(models.Model):
    name = models.CharField(verbose_name=_('Tipo de Héroe'), max_length=25, null=False, blank=False, unique=True)
    code = models.CharField(verbose_name=_('Código'), max_length=1, null=False, blank=False, unique=True)

    class Meta:
        verbose_name = _('Tipo de Héroe')
        verbose_name_plural = _('Tipos de Héroes')

    def __str__(self):
        return self.name


class TypeAttack(models.Model):
    name = models.CharField(verbose_name=_('Tipo de Ataque'), max_length=25, null=False, blank=False, unique=True)
    code = models.CharField(verbose_name=_('Código'), max_length=1, null=False, blank=False, unique=True)

    class Meta:
        verbose_name = _('Tipo de Ataque')
        verbose_name_plural = _('Tipos de Ataques')

    def __str__(self):
        return self.name


class Player(models.Model):
    name = models.CharField(max_length=50, verbose_name='Nombre')
    userprof = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, default=None)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ('name', )
        verbose_name = 'Jugador'
        verbose_name_plural = 'Jugadores'


class Skill(models.Model):
    name = models.CharField(max_length=70, verbose_name='Nombre')
    description = models.TextField(max_length=200, verbose_name='Efecto')
    imagen = models.ImageField('Logo', upload_to=scramble_upload_avatar, default=None, null=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Habilidad'
        verbose_name_plural = 'Habilidades'

    def __str__(self):
        return self.name


class Hero(models.Model):
    name = models.CharField(max_length=50, verbose_name='Nombre', help_text='Nombre del h€roe que se muestra.')
    slug = models.CharField(max_length=50, verbose_name='Slug',
                            help_text='Nombre con que se identifica el h€roe en los logs.')
    team = models.ForeignKey(TypeTeam, default='', on_delete=models.CASCADE,
                             verbose_name='Equipo', help_text='Equipo o Facción al que pertenece el héroe.')
    type = models.ForeignKey(TypeHero, default='', on_delete=models.CASCADE,
                             verbose_name='Tipo', help_text='Tipo del héroe')
    atack = models.ForeignKey(TypeAttack, verbose_name='Ataca', on_delete=models.CASCADE,
                              help_text='Si el héroe ataca de rango o no')
    image = models.ImageField('Avatar', upload_to=scramble_upload_avatar,
                              help_text='Avatar del héroe, que se muestra en la lista.', default=None, null=True)
    background = models.ImageField('Background', upload_to=scramble_upload_background, null=True,
                                   help_text='Background mostrado en la pagina de detalles del héroe.', default='')
    detail_pic = models.ImageField('Detalle', upload_to=scramble_upload_detail, null=True,
                                   help_text="Imagen con una descripción del héroe, sus habilidades y recomendaciones.",
                                   default='')
    skills = models.ManyToManyField(Skill, blank=True, default='', verbose_name="habilidades")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name', )
        verbose_name_plural = 'Heroes'
        verbose_name = 'Heroe'

    def check_skills(self):
        if self.skills.count() > 4:
            last = self.skills.last()
            last.delete()
            self.check_skills()
        return

    def remove_skill(self, id_skill):
        sk = self.skills.filter(id=id_skill).first()
        sk.delete()


class Game(models.Model):
    match_id = models.CharField(max_length=10, blank=True, null=True)
    server_game_name = models.CharField(max_length=100, blank=True, null=True)
    game_name = models.CharField(max_length=60, blank=True, null=True)
    game_version = models.CharField(max_length=10, blank=True, null=True)
    match_name = models.CharField(max_length=50, blank=True, null=True)
    map_name = models.CharField(max_length=50, blank=True, null=True)
    map_version = models.CharField(max_length=10, blank=True, null=True)
    match_date = models.DateField(auto_now_add=False, blank=True, null=True)
    match_time = models.TimeField(auto_now_add=False, blank=True, null=True)
    log_file = models.FileField('Archivo Log', upload_to=scramble_upload_log)
    team_win = models.ForeignKey(TypeTeam, on_delete=models.CASCADE, null=True, blank=True, default='')
    win_time = models.PositiveIntegerField(null=True, blank=True, default=0)

    players_onplay = models.ManyToManyField(Player, related_name='players_onplay', through='PlayersGame', blank=True)

    def __str__(self):
        return self.match_name + ' -> ' + str(self.match_date)

    class Meta:
        ordering = ('match_date', )
        verbose_name = 'Juego'
        verbose_name_plural = 'Juegos'

    def parse_c_log_data(self):

        try:
            f = open(settings.MEDIA_ROOT + '/' + str(self.log_file), 'r', encoding='utf-8')
            data = f.readlines()
        except:
            f = open(settings.MEDIA_ROOT + '/' + str(self.log_file), 'r', encoding='latin-1')
            encoded_data = f.readlines()
            data = []
            for line in encoded_data:
                lineu = line.encode('utf-8').decode('utf-8').replace('\x00', '')
                data.append(lineu)

        start_time = time.time()
        start_in = 0
        step = len(data) // NUM_WORKERS
        stop_in = start_in + step

        threads = []
        game_data = ParserGame()
        for _ in range(NUM_WORKERS):
            threads.append(threading.Thread(target=parse_data,
                                            args=(data, game_data, ),
                                            kwargs={'start': int(start_in),
                                                    'end': int(stop_in)}))
            start_in += step
            stop_in += step
            print(stop_in, "lineas" )
        [thread.start() for thread in threads]
        [thread.join() for thread in threads]
        end_time = time.time()
        print("Threads time=", end_time - start_time)
        if self.verify_parse(game_data):
            self.save_parse(game_data)

    def verify_parse(self, data):
        if len(data.playersgame_set) < 6:
            self.delete()
            raise ValidationError(message=_('El log no será salvado porque el juego es de menos de 6 jugadores'))
        if Game.objects.filter(match_date=data.match_date, match_time=data.match_time, match_id=data.match_id).exists():
            self.delete()
            raise ValidationError(message=_('El log no será salvado porque ya existe este juego salvado en la base de datos'))
        return True

    def save_parse(self, data):
        self.game_name = data.game_name
        self.game_version = data.game_version
        self.map_name = data.map_name
        self.map_version = data.map_version
        self.match_id = data.match_id
        self.match_name = data.match_name
        self.match_date = datetime.date(year=int(data.match_date.split('-')[0]),
                                        month=int(data.match_date.split('-')[-1]),
                                        day=int(data.match_date.split('-')[1]))
        self.match_time = datetime.time(hour=int(data.match_time.split(':')[0]),
                                        minute=int(data.match_time.split(':')[1]),
                                        second=int(data.match_time.split(':')[-1]))
        self.team_win = TypeTeam.objects.filter(code=data.team_win).first()
        self.win_time = data.win_time
        self.server_game_name = data.server_game_name
        for player_on_game in data.playersgame_set:
            player, created = Player.objects.get_or_create(name=player_on_game.player)
            team, created = TypeTeam.objects.get_or_create(code=player_on_game.team)
            hero = Hero.objects.filter(slug=player_on_game.hero).first()
            playergame = PlayersGame()
            playergame.player = player
            playergame.player_pos = player_on_game.player_pos
            playergame.game = self
            playergame.team = team
            playergame.hero = hero
            playergame.kills = player_on_game.kills
            playergame.dead = player_on_game.dead
            playergame.assitances = player_on_game.assitances
            playergame.golds = player_on_game.golds
            playergame.experiens = player_on_game.experiens
            playergame.damage = player_on_game.damage
            playergame.firstblood = player_on_game.firstblood
            playergame.firstblood_die = player_on_game.firstblood_die
            playergame.ip_address = player_on_game.ip_address
            playergame.save()

    def check_parse(self):
        if self.match_time and self.match_name and self.match_id and self.server_game_name and self.game_name and self.map_name and self.players_onplay.count() > 0:
            return True
        else:
            return False

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super(Game, self).save()
        self.parse_c_log_data()
        if not self.check_parse():
            self.delete()
            raise ValidationError('El archivo log no pudo ser analizado, revise si subió el archivo correcto.')
        return super(Game, self).save()


class PlayersGame(models.Model):
    ip_address = models.CharField(max_length=17, blank=True, null=True)
    hero = models.ForeignKey(Hero, on_delete=models.CASCADE, blank=True, null=True)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    player_pos = models.IntegerField(default=100, blank=True, null=True)
    team = models.ForeignKey(TypeTeam, on_delete=models.CASCADE, default='', blank=True, null=True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, default='')
    kills = models.PositiveIntegerField(blank=True, null=True, default=0)
    dead = models.PositiveIntegerField(blank=True, null=True, default=0)
    experiens = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, default=0)
    golds = models.IntegerField(blank=True, null=True, default=0)
    assitances = models.PositiveIntegerField(blank=True, null=True, default=0)
    damage = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, default=0)
    firstblood = models.CharField(max_length=10, blank=True, null=True, default='')
    firstblood_die = models.CharField(max_length=10, blank=True, null=True, default='')

    def __str__(self):
        return '{}'.format(self.player)

    class Meta:
        verbose_name = 'Jugador en Juego'
        verbose_name_plural = 'Jugadores en Juego'

    def check_have_data(self):
        if self.damage == 0 and self.assitances == 0 and self.golds == 0 and self.experiens == 0 and self.dead == 0 and self.kills == 0 and self.team == '' and self.firstblood == '':
            return False
        else:
            return True


class Item(models.Model):
    name = models.CharField(max_length=70, verbose_name="Nombre")
    description = models.TextField(max_length=300, verbose_name="Efecto")
    imagen = models.ImageField('Imagen', upload_to=scramble_upload_avatar, null=True, default=None)

    class Meta:
        ordering = ('name', )
        verbose_name = 'Objeto'
        verbose_name_plural = 'Objetos'

    def __str__(self):
        return self.name


class Strategic(models.Model):
    name = models.CharField(max_length=75, verbose_name="Nombre")
    hero = models.ForeignKey(Hero, on_delete=models.CASCADE, verbose_name="Héroe")
    skills = models.ManyToManyField(Skill, blank=True, through='LvlSkill', through_fields=('strategic', 'skill'))
    items = models.ManyToManyField(Item, blank=True, through='ItemStrategic', through_fields=('strategic', 'item'))
    description = models.TextField(max_length=600)

    class Meta:
        ordering = ('name', 'hero__name', )
        verbose_name = 'Estrategia'
        verbose_name_plural = 'Estrategias'

    def __str__(self):
        return self.name


class LvlSkill(models.Model):
    strategic = models.ForeignKey(Strategic, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.SET_DEFAULT, default=None, null=True)
    lvl_number = models.PositiveSmallIntegerField(verbose_name="Nivel")


class ItemStrategic(models.Model):
    strategic = models.ForeignKey(Strategic, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.SET_DEFAULT, default=None, null=True)
    item_time = models.IntegerField(choices=ITEM_CHOISE, default=1, verbose_name='Momento del objeto', help_text='Momento de juego en que se debe obtener el objeto.')