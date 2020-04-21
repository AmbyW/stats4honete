from django.apps import AppConfig


class ThingsConfig(AppConfig):
    name = 'things'

    def ready(self):
        pass
        # verify
        # TypeAttack.objects.bulk_create([TypeAttack(name='Melee', code='1'), TypeAttack(name='Rango', code='2')])
        # TypeHero.objects.bulk_create([TypeHero(name='Agilidad', code='1'), TypeHero(name='Fuerza', code='2'), TypeHero(name='Inteligencia', code='3')])
        # TypeTeam.objects.bulk_create([TypeTeam(name='HellBourne', code='1'), TypeTeam(name='Legion', code='2')])
