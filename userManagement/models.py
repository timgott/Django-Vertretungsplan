from django.db import models
from customUser.models import SiteUser

from .validators import UnicodeClassValidator

class SchuelerProfile(models.Model):
    validator = UnicodeClassValidator()
    user = models.OneToOneField(SiteUser, on_delete=models.CASCADE)
    klasse = models.CharField(max_length = 3, 
        verbose_name= 'Klasse',
        help_text=('Muss die Klasse sein nicht der Kurs!.'),
        validators = [validator],
        blank = True
        )
    kurse = models.CharField(max_length = 150, verbose_name = 'Kurs', blank = True)

    def __str__(self):
        return f'{self.user.username} Schüler Profil'

class LehrerProfile(models.Model):
    user = models.OneToOneField(SiteUser, on_delete=models.CASCADE)
    kuerzel = models.CharField(max_length = 4, 
        verbose_name = 'Lehrer Kürzel',
        help_text = ('Ihr Kürzel als Lehrer.'),
        blank = True,
        )
    
    def __str__(self):
        return f'{self.user.username} Lehrer Profil'

