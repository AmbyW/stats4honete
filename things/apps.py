from django.apps import AppConfig
from django.conf import settings
from django.contrib.auth import get_user_model

from .utils import is_database_synchronized


class ThingsConfig(AppConfig):
    name = 'things'

    def ready(self):
        if is_database_synchronized():
            check_and_create_initial_models()
            check_and_create_default_superuser()


def check_and_create_initial_models():
    try:
        from .models import TypeAttack, TypeHero, TypeTeam
        TypeAttacks = [('Melee', '1'), ('Rango', '2'), ]
        TypeHeroes = [('Agilidad', '1'), ('Fuerza', '2'), ('Inteligencia', '3'), ]
        TypeTeams = [('HellBourne', '1'), ('Legion', '2'), ]
        check_and_create_models(TypeTeam, TypeTeams)
        check_and_create_models(TypeHero, TypeHeroes)
        check_and_create_models(TypeAttack, TypeAttacks)

    except ImportError as _:
        pass


def check_and_create_models(model_class, values):
    [model_class.objects.create(name=value[0], code=value[1]) for value in values
     if not model_class.objects.filter(name=value[0], code=value[1]).exists()]


def check_and_create_default_superuser():

    if hasattr(settings, 'DEFAULT_SUPERUSER_NAME') and settings.DEFAULT_SUPERUSER_NAME \
            and hasattr(settings, 'DEFAULT_SUPERUSER_PASS') and settings.DEFAULT_SUPERUSER_PASS:
        username = settings.DEFAULT_SUPERUSER_NAME
        password = settings.DEFAULT_SUPERUSER_PASS
        UserModel = get_user_model()
        if not UserModel.objects.filter(username=username).exists():
            superuser = UserModel(username=username)
            superuser.set_password(password=password)
            superuser.save()
