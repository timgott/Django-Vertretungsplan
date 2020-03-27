from django.db import models

# Create your models here.

class Vplan_schueler(models.Model):
    pos = models.IntegerField(verbose_name="Unterichtsstunde")
    fach = models.CharField(max_length=100, verbose_name="Fach")
    raum = models.CharField(max_length=100, verbose_name="Raum")
    klasse = models.CharField(max_length=100, verbose_name="Klasse")
    info = models.CharField(max_length=100, verbose_name="Informationen")
    art = models.CharField(max_length=100, verbose_name="Art")   