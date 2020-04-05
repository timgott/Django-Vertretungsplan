from django import forms
from django.contrib.auth.forms import UserCreationForm 
from django.conf import settings

from customUser.models import SiteUser

from .models import SchuelerProfile
from .validators import class_validator

class SchuelerProfileUpdateForm(forms.ModelForm):
    klasse = forms.CharField(validators=[class_validator])
    class Meta:
        model = SchuelerProfile
        fields = ['klasse', 'kurse']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = SiteUser
        fields = ['username', 'email']

