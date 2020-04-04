from django.contrib import admin

from .models import SchuelerProfile, LehrerProfile

admin.site.register(SchuelerProfile)
admin.site.register(LehrerProfile)