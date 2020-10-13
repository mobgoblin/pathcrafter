import json

from django import forms
from .models import PostAd

CATEGORIES = (
    ('LAB', 'labor'),
    ('CAR', 'cars'),
    ('TRU', 'trucks'),
    ('WRI', 'writing'),
)
LOCATIONS = (
    ('BRO', 'Bronx'),
    ('BRK', 'Brooklyn'),
    ('QNS', 'Queens'),
    ('MAN', 'Manhattan'),
)

data = {}
list = ()

with open('spells.txt') as json_file:
    data = json.load(json_file)
    index = 0
    for key in data:
        list += (('SP' + str(index), key),)
        index += 1

class PostAdForm(forms.ModelForm):
    error_css_class = 'error'

    category = forms.ChoiceField(choices=list, required=True )
    location = forms.ChoiceField(choices=LOCATIONS, required=True )

    class Meta:
        model = PostAd
        fields = '__all__'

        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'What\'s your name?'}),
            'email': forms.TextInput(attrs={'placeholder': 'john@example.com'}),
            'gist': forms.TextInput(attrs={'placeholder': 'In a few words, I\'m looking for/to...'}),
            'expire': forms.TextInput(attrs={'placeholder': 'MM/DD/YYYY'})
        }