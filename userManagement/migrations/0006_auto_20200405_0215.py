# Generated by Django 3.0.2 on 2020-04-05 00:15

from django.db import migrations, models
import userManagement.validators


class Migration(migrations.Migration):

    dependencies = [
        ('userManagement', '0005_auto_20200404_2317'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schuelerprofile',
            name='klasse',
            field=models.CharField(blank=True, help_text='Muss die Klasse sein nicht der Kurs!.', max_length=3, validators=[userManagement.validators.class_validator], verbose_name='Klasse'),
        ),
    ]
