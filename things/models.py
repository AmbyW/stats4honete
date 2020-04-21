from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.db.models import Q, F
from django.core.exceptions import ValidationError, MultipleObjectsReturned
import uuid
from statshon import settings
import datetime
import time

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

    def parse_log_data(self):
        b = 0
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

        start_in = 0
        step = len(data)//NUM_WORKERS
        stop_in = start_in + step

        f.close()
        start_time = time.time()
        for l in data:
            if 'INFO_DATE' in l:
                self.parse_datetime(l)
            if 'INFO_GAME' in l:
                self.parse_info_game(l)
            if 'INFO_MATCH' in l:
                self.parse_info_match(l)
            if 'INFO_MAP' in l:
                self.parse_info_map(l)
            if 'INFO_SERVER' in l:
                self.parse_info_server(l)
            if str(l).startswith('GAME_START'):
                self.parse_start(data[-3:])
            if str(l).startswith('PLAYER_CONNECT'):
                print(l)
                self.parse_player_conn(l)
            if str(l).startswith('PLAYER_TEAM_CHANGE'):
                self.parse_teamchange(l)
            if str(l).startswith('KILL'):
                self.parse_kill(l)
            if str(l).startswith('AWARD_FIRST_BLOOD'):
                self.parse_first(l)
            if str(l).startswith('EXP_EARNED'):
                self.parse_exp(l)
            if str(l).startswith('GOLD_EARNED'):
                self.parse_gold_plus(l)
            if str(l).startswith('GOLD_LOST'):
                self.parse_gold_less(l)
            if str(l).startswith('DAMAGE'):
                self.parse_damage(l)
        end_time = time.time()
        print("Used time=", end_time - start_time)

    def parse_info_game(self, line):
        l = line.split("\"")
        self.game_name = l[1]
        self.game_version = l[3]

    def parse_info_match(self, line):
        l = line.split("\"")
        self.match_name = l[1]
        self.match_id = l[3]

    def parse_info_map(self, line):
        l = line.split("\"")
        self.map_name = l[1]
        self.map_version = l[3]

    def parse_info_server(self, line):
        l = line.split("\"")
        self.server_game_name = l[1]

    def parse_player_conn(self, line):
        l1 = line.split("\"")
        l2 = line.split(":")
        print('l1', l1)
        print('l2', l2)
        player_pos = ''
        for u in range(len(l2)):
            if 'player' in l2[u]:
                player_pos = l2[u+1].split(' ')[0]
                print('pos', player_pos)
        player = Player.objects.get_or_create(name=l1[1])[0]
        print('pl', player)
        pop, created = self.playersgame_set.get_or_create(player=player, game=self, defaults={'ip_address': l1[3],
                                                                                              'player_pos': player_pos})
        print('pop', pop)
        pop.ip_address = l1[3]
        print('addr', l1[3])
        pop.player_pos = player_pos
        pop.save()

    def parse_teamchange(self, line):
        l1 = line.split(":")
        team = TypeTeam.objects.filter(code=l1[-1].replace('\n', '')).first()
        try:
            pop = self.playersgame_set.update_or_create(game=self,
                                                        player_pos=l1[1].split(' ')[0],
                                                        defaults={'team': team})
        except MultipleObjectsReturned as e:
            pop = self.playersgame_set.filter(game=self, player_pos=l1[1].split(' ')[0],).first()
            pop.team = team
            pop.save()

    def parse_kill(self, line):
        who_kill = ''
        hero_kill = ''
        hero_die = ''
        who_die = ''
        who_assist = []
        l = line.split(":")
        for u in range(len(l)):
            if 'player' in l[u]:
                who_kill = l[u+1].split(' ')[0]
            if 'owner' in l[u]:
                who_die = l[u+1].split(' ')[0]
            if 'assists' in l[u]:
                who_assist = l[u+1].replace('\n', '').split(',')
            if 'target' in l[u]:
                hero_die = l[u+1].replace('"', '').split(' ')[0]
            if 'attacker' in l[u]:
                hero_kill = l[u+1].replace('"', '').split(' ')[0]
        if hero_die.startswith('Hero_') and hero_kill.startswith('Hero_'):
            pop = PlayersGame.objects.filter(game=self).filter(player_pos=who_kill).first()
            pop.kills += 1
            if not pop.hero:
                pop.hero = Hero.objects.filter(slug=hero_kill).first()
            pop.save()
            pop = PlayersGame.objects.filter(game=self).filter(player_pos=who_die).first()
            pop.dead += 1
            if not pop.hero:
                pop.hero = Hero.objects.filter(slug=hero_die).first()
            pop.save()
            for asister in who_assist:
                pop = PlayersGame.objects.filter(game=self).filter(player_pos=asister).first()
                pop.assitances += 1
                pop.save()
        if hero_die.startswith('Hero_') and not hero_kill.startswith('Hero_'):
            pop = PlayersGame.objects.filter(game=self).filter(player_pos=who_die).first()
            pop.dead += 1
            if not pop.hero:
                pop.hero = Hero.objects.filter(slug=hero_die).first()
            pop.save()
            if hero_kill.startswith('Gadget_Assist'):
                pop = PlayersGame.objects.filter(game=self).filter(player_pos=who_kill).first()
                pop.kills += 1
                pop.save()
            for asister in who_assist:
                pop = PlayersGame.objects.filter(game=self).filter(player_pos=asister).first()
                pop.assitances += 1
                pop.save()

    def parse_first(self, line):
        l = line.split(":")
        player_pos = ''
        player_die_pos = ''
        hero_slug = ''
        time = ''
        for u in range(len(l)):
            if 'time' in l[u]:
                time = l[u+1].split(' ')[0]
            if 'player' in l[u]:
                player_pos = l[u+1].split(' ')[0]
            if 'owner' in l[u]:
                player_die_pos = l[u+1].split(' ')[0]
            if 'name' in l[u]:
                hero_slug = l[u+1].replace('"', '').split(' ')[0]
        if player_pos != '':
            pop = PlayersGame.objects.filter(game=self, player_pos=player_pos).first()
            pop.firstblood = time
            if not pop.hero and hero_slug != '':
                pop.hero = Hero.objects.filter(slug=hero_slug).first()
            pop.save()
        if player_die_pos != '':
            pop = PlayersGame.objects.filter(game=self, player_pos=player_die_pos).first()
            pop.firstblood_die = time
            pop.save()

    def parse_gold_plus(self, line):
        l = line.split(":")
        player_pos = ''
        gold = ''
        for u in range(len(l)):
            if 'player' in l[u]:
                player_pos = l[u+1].split(' ')[0]
            if 'gold' in l[u]:
                gold = l[u+1].split(' ')[0]
        gold = gold.replace('\n', '')
        if player_pos != '':
            pop = PlayersGame.objects.filter(game=self, player_pos=player_pos).first()
            pop.golds += float(gold)
            pop.save()

    def parse_gold_less(self, line):
        l = line.split(":")
        player_pos = ''
        gold = ''
        for u in range(len(l)):
            if 'player' in l[u]:
                player_pos = l[u+1].split(' ')[0]
            if 'gold' in l[u]:
                gold = l[u+1].split(' ')[0]
        gold = gold.replace('\n', '')
        if player_pos != '':
            pop = PlayersGame.objects.filter(game=self, player_pos=player_pos).first()
            pop.golds -= float(gold)
            pop.save()

    def parse_damage(self, line):
        l = line.split(":")
        player_pos = ''
        damage = ''
        hero = ''
        for u in range(len(l)):
            if 'player' in l[u]:
                player_pos = l[u+1].split(' ')[0]
            if 'damage' in l[u]:
                damage = l[u+1].split(' ')[0]
            if 'attacker' in l[u]:
                hero = l[u+1].replace('"', '').split(' ')[0]
        if player_pos != '':
            pop = PlayersGame.objects.filter(game=self, player_pos=player_pos).first()
            pop.damage = float(damage)
            if not pop.hero:
                pop.hero = Hero.objects.filter(slug=hero).first()
            pop.save()

    def parse_exp(self, line):
        l = line.split(":")
        player_pos = ''
        exp = ''
        for u in range(len(l)):
            if 'player' in l[u]:
                player_pos = l[u+1].split(' ')[0]
            if 'experience' in l[u]:
                exp = l[u+1].split(' ')[0]
        if player_pos != '':
            pop = PlayersGame.objects.get(game=self, player_pos=player_pos)
            pop.experiens = float(exp)
            pop.save()

    def parse_datetime(self, line):
        l = line.split("\"")
        date = l[1]
        time = l[3]
        self.match_date = datetime.date(year=int(date.split('/')[0]), month=int(date.split('/')[-1]), day=int(date.split('/')[1]))
        self.match_time = datetime.time(hour=int(time.split(':')[0]), minute=int(time.split(':')[1]))

    def parse_end(self, endlines):
        is_finish = False
        for l in endlines:
            if 'GAME_END' in l:
                is_finish = True
                team = TypeTeam.objects.filter(code=l.split('\"')[-2]).first()
                self.team_win = team
                self.win_time = int(l.split(':')[1].split(' ')[0])
        if not is_finish:
            self.delete()
            raise ValidationError('El juego no esta terminado', code='endless_game')
        
    def parse_start(self, endli):
        if self.playersgame_set.count() < 6:
            self.delete()
            raise ValidationError('Menos de los jugadores necesarios', code='few_players')
        if Game.objects.exclude(id=self.id).filter(match_date=self.match_date, match_time=self.match_time, server_game_name=self.server_game_name).exists():  
            self.delete()
            raise ValidationError('Ya a sido subido esta juego', code='already_exist')
        self.parse_end(endli)

    def check_parse(self):
        if self.match_time and self.match_name and self.match_id and self.server_game_name and self.game_name and self.map_name and self.players_onplay.count() > 0:
            return True
        else:
            return False

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super(Game, self).save()
        self.parse_log_data()
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