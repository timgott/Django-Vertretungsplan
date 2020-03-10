from django import forms
from customUser.models import SiteUser
from django.contrib.auth.forms import UserCreationForm 
from django.conf import settings

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    #class Meta:
    #    #model = settings.AUTH_USER_MODEL
    #    fields = ['username', 'email', 'password1', 'password2',]