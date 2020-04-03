from django.db import models
from customUser.models import SiteUser

from .validators import UnicodeClassValidator

class Profile(models.Model):
    validator = UnicodeClassValidator()
    user = models.OneToOneField(SiteUser, on_delete=models.CASCADE)
    klasse = models.CharField(max_length = 3, 
        verbose_name= 'Klasse',
        help_text=('Muss die Klasse sein nicht der Kurs!.'),
        validators = [validator],
        blank = True
        )
    kurs = models.CharField(max_length = 10, verbose_name = 'Kurs', blank = True)


    def __str__(self):
        return f'{self.user.username} Profil'
