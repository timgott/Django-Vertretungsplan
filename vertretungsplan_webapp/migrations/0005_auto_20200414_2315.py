# Generated by Django 3.0.2 on 2020-04-14 21:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vertretungsplan_webapp', '0004_auto_20200401_0153'),
    ]

    operations = [
        migrations.AddField(
            model_name='vplan',
            name='vplanType',
            field=models.CharField(default='schueler', max_length=8, verbose_name='Typ des Vplans'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='vplanschuelerentry',
            name='vplan',
            field=models.ForeignKey(limit_choices_to={'vplanType': 'schueler'}, on_delete=django.db.models.deletion.CASCADE, to='vertretungsplan_webapp.Vplan'),
        ),
        migrations.CreateModel(
            name='VplanLehrerEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pos', models.IntegerField(verbose_name='Unterichtsstunde')),
                ('fach', models.CharField(max_length=100, verbose_name='Fach')),
                ('raum', models.CharField(max_length=100, verbose_name='Raum')),
                ('klasse', models.CharField(max_length=10, verbose_name='Klasse')),
                ('art', models.CharField(max_length=100, verbose_name='Art')),
                ('lehrer', models.CharField(max_length=100, verbose_name='Lehrer')),
                ('lehrerName', models.CharField(max_length=4, verbose_name='Name des zugehörigen Lehrer')),
                ('vplan', models.ForeignKey(limit_choices_to={'vplanType': 'lehrer'}, on_delete=django.db.models.deletion.CASCADE, to='vertretungsplan_webapp.Vplan')),
            ],
        ),
    ]
