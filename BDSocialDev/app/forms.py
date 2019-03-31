"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from .tags import (_hashtags_fitness, _hashtags_food, _hashtags_travel,
                  _hashtags_tech, _hashtags_fashion, _hashtags_Influencer)

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))
    from django import forms

class SearchFormFitnes(forms.Form):
    fitnes = forms.ChoiceField(choices=_hashtags_fitness)

class SearchFormFood(forms.Form):
    food = forms.ChoiceField(choices=_hashtags_food)

class SearchFormTravel(forms.Form):
    travel = forms.ChoiceField(choices=_hashtags_travel)

class SearchFormTech(forms.Form):
    tech = forms.ChoiceField(choices=_hashtags_tech)

class SearchFormFashion(forms.Form):
    fashion = forms.ChoiceField(choices=_hashtags_fashion)

class SearchFormInfluencer(forms.Form):
    area_influencer = forms.ChoiceField(choices=_hashtags_Influencer)

