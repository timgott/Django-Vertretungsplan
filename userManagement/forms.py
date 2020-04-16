from django import forms
from django.contrib.auth.forms import UserCreationForm 
from django.conf import settings

from customUser.models import SiteUser

from .models import SchuelerProfile, LehrerProfile

class SchuelerProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = SchuelerProfile
        fields = ['klasse', 'kurse']

class LehrerProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = LehrerProfile
        fields = ['kuerzel']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = SiteUser
        fields = ['username', 'email']

