from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.
class HonStatSettings(models.Model):
    teamspeak_srv_url = models.CharField(max_length=500,
                                         verbose_name=_('Url Servidor TeamSpeak'),
                                         default='',
                                         help_text=_('Dirección Url del servidor TeamSpeak usado para jugar'),
                                         blank=True)
    color_first_place = models.CharField(max_length=10,
                                         verbose_name=_('Color Primer Lugar'),
                                         help_text=_('Color the fuente del jugador que se encuentra en primer lugar en '
                                                     'las estadisticas'),
                                         default='green',
                                         blank=True)
    color_positive_ranking = models.CharField(max_length=10,
                                              verbose_name=_('Color Ranking positivo'),
                                              help_text=_('Color the fuente del jugador cuyo promedio de puntuación '
                                                          'es positivo'),
                                              default='blue',
                                              blank=True)
    color_negative_ranking = models.CharField(max_length=10,
                                              verbose_name=_('Color Ranking negativo'),
                                              help_text=_('Color the fuente del jugador cuyo promedio de puntuación '
                                                          'es negativo'),
                                              default='red',
                                              blank=True)
    color_last_place = models.CharField(max_length=10,
                                        verbose_name=_('Color Último Lugar'),
                                        help_text=_('Color the fuente del jugador que ocupa el último lugar en las '
                                                    'estadíticas'),
                                        default='brown',
                                        blank=True)
    min_games = models.PositiveSmallIntegerField(_('Mínimo de Juegos'),
                                                 default=20,
                                                 blank=True,
                                                 help_text=_('Es el minimo de juegos que debe tener un jugador para '
                                                             'calcular su promedio de puntos por los juegos jugados, '
                                                             'en cambio si el jugado no tiene al menos ese numero de '
                                                             'juegos jugados su promedio se calculará con ese número'))
    kill_value = models.FloatField(_('Peso del Asesinato'),
                                   default=0.5,
                                   blank=True,
                                   help_text=_('Valor o Peso que tiene cometer un asesianto en una partida, la '
                                               'modicación de este valor puede hacer que la acción de asesinar '
                                               'tome mayor o menor relevancia en las estadísticas'))
    dead_value = models.FloatField(_('Peso de Muerte'),
                                   default=-0.3,
                                   blank=True,
                                   help_text=_('Valor o Peso que tiene ser asesinado en una partida, la '
                                               'modicación de este valor puede hacer que la acción de morir '
                                               'tome mayor o menor relevancia en las estadísticas'))
    assist_value = models.FloatField(_('Peso de la Asistencia'),
                                     default=-0.25,
                                     blank=True,
                                     help_text=_('Valor o Peso que tiene realizar una asistencia en una partida, la '
                                                 'modicación de este valor puede hacer que dicha acción tome mayor o '
                                                 'menor relevancia en las estadísticas'))
    fkill_value = models.FloatField(_('Peso de Primer Asesinato'),
                                    default=0.6,
                                    blank=True,
                                    help_text=_('Valor o Peso que tiene cometer el primer asesinato en una partida, la '
                                                'modicación de este valor puede hacer que esta acción tome mayor o '
                                                'menor relevancia en las estadísticas'))
    fdead_value = models.FloatField(_('Peso de Primera Muerte'),
                                    default=-0.5,
                                    blank=True,
                                    help_text=_('Valor o Peso que tiene ser el primer asesinado en una partida, la '
                                                'modicación de este valor puede hacer que esta acción tome mayor o '
                                                'menor relevancia en las estadísticas'))
    win_value = models.FloatField(_('Peso de la Vitoria'),
                                  default=0.8,
                                  blank=True,
                                  help_text=_('Valor o Peso que tiene ganar una partida, la modicación de este valor '
                                              'puede hacer que esta acción tome mayor o menor relevancia en las '
                                              'estadísticas'))
    loose_value = models.FloatField(_('Peso de la Derrota'),
                                    default=-0.4,
                                    blank=True,
                                    help_text=_('Valor o Peso que tiene ser derrotado en una partida, la modicación de '
                                                'este valor puede hacer que esta acción tome mayor o menor relevancia '
                                                'en las estadísticas'))

    class Meta:
        verbose_name = 'HoN stats App settings'

    def __str__(self):
        return _('HoN stats App settings')

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.pk = 1
        self.id = 1
        return super().save(force_insert, force_update, using, update_fields)
