from django.db import models

# Create your models here.

class Vplan(models.Model):
    vplanDate = models.DateField(verbose_name = 'Vertretungsplan Datum')
    vplanUploadDate = models.DateTimeField(auto_now_add = True, verbose_name = 'Vertretungsplan Uploaddatum')
    vplanType = models.CharField(max_length = 8, verbose_name = 'Typ des Vplans')

class VplanSchuelerEntry(models.Model):
    vplan = models.ForeignKey(Vplan,
        on_delete = models.CASCADE,
        limit_choices_to = {'vplanType': 'schueler'},
        related_name = 'schueler',
        )

    pos = models.IntegerField(verbose_name='Unterichtsstunde')
    fach = models.CharField(max_length=100, verbose_name='Fach')
    raum = models.CharField(max_length=100, verbose_name='Raum')
    klasse = models.CharField(max_length=10, verbose_name='Klasse')
    info = models.CharField(max_length=100, verbose_name='Informationen')
    art = models.CharField(max_length=100, verbose_name='Art')   

class VplanLehrerEntry(models.Model):
    vplan = models.ForeignKey(Vplan,
        on_delete= models.CASCADE,
        limit_choices_to = {'vplanType': 'lehrer'}, 
        related_name = 'lehrer',
        )

    pos = models.IntegerField(verbose_name='Unterichtsstunde')
    fach = models.CharField(max_length=100, verbose_name='Fach')
    raum = models.CharField(max_length=100, verbose_name='Raum')
    klasse = models.CharField(max_length=10, verbose_name='Klasse')
    art = models.CharField(max_length=100, verbose_name='Art')
    lehrer = models.CharField(max_length=100, verbose_name='Lehrer')
    lehrerName = models.CharField(max_length=4, verbose_name='Name des zugehörigen Lehrer')