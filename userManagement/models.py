from django.db import models
from customUser.models import SiteUser

class Profile(models.Model):
    user = models.OneToOneField(SiteUser, on_delete=models.CASCADE)
    klasse = models.CharField(max_length = 3, verbose_name= 'Klasse')
    kurs = models.CharField(max_length = 5, verbose_name = 'Kurs')


    def __str__(self):
        return f'{self.user.username} Profil'
