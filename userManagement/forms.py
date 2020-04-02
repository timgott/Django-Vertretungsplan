from django import forms
from django.contrib.auth.forms import UserCreationForm 
from django.conf import settings

from customUser.models import SiteUser

from .models import Profile

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = SiteUser
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['klasse', 'kurs']