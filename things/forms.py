from django import forms
from .models import Game, Hero


# Put your forms here
class GameForm(forms.ModelForm):

    class Meta:
        model = Game
        fields = ('log_file', )

    widgets = {
        'log_file': forms.FileInput(attrs={"class": "redbtn"}),
    }


class HeroForm(forms.ModelForm):

    class Meta:
        model = Hero
        fields = ('name', 'slug', 'type', 'atack', 'team', 'image', 'background', 'detail_pic', )

