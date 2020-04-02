from django.db import models

# Create your models here.

class Vplan(models.Model):
    vplanDate = models.DateField(verbose_name = 'Vertretungsplan Datum')
    vplanUploadDate = models.DateTimeField(auto_now_add = True,verbose_name = 'Vertretungsplan Uploaddatum')

class VplanSchuelerEntry(models.Model):
    vplan = models.ForeignKey('Vplan', on_delete = models.CASCADE)
    
    pos = models.IntegerField(verbose_name='Unterichtsstunde')
    fach = models.CharField(max_length=100, verbose_name='Fach')
    raum = models.CharField(max_length=100, verbose_name='Raum')
    klasse = models.CharField(max_length=10, verbose_name='Klasse')
    info = models.CharField(max_length=100, verbose_name='Informationen')
    art = models.CharField(max_length=100, verbose_name='Art')   
    