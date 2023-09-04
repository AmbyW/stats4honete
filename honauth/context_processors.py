from django.forms.models import model_to_dict

from .models import HonStatSettings


def hon_app_settings(request):
    preferences = HonStatSettings.objects.get_or_create(id=1)
    selected_fields = ['teamspeak_srv_url',
                       'color_first_place',
                       'color_positive_ranking',
                       'color_negative_ranking',
                       'color_last_place',
                       'min_games',
                       'kill_value',
                       'dead_value',
                       'assist_value',
                       'fkill_value',
                       'fdead_value',
                       'win_value',
                       'loose_value', ]
    return model_to_dict(preferences, fields=selected_fields)
