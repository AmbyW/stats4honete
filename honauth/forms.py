from django import forms

from .widgets import ColorInput
from .models import HonStatSettings


class HonStatSettingsForm(forms.ModelForm):
    color_first_place = forms.CharField(widget=ColorInput)
    color_positive_ranking = forms.CharField(widget=ColorInput)
    color_negative_ranking = forms.CharField(widget=ColorInput)
    color_last_place = forms.CharField(widget=ColorInput)

    class Meta:
        model = HonStatSettings
        fields = ['color_first_place',
                  'color_positive_ranking',
                  'color_negative_ranking',
                  'color_last_place',
                  'teamspeak_srv_url',
                  'min_games',
                  'kill_value',
                  'dead_value',
                  'assist_value',
                  'fkill_value',
                  'fdead_value',
                  'win_value',
                  'loose_value', ]
