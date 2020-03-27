from django import forms
from customUser.models import SiteUser
from django.contrib.auth.forms import UserCreationForm 
from django.conf import settings

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = SiteUser
        fields = ['username', 'email']
