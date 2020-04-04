from django.db.models.signals import post_save
from customUser.models import SiteUser
from django.dispatch import receiver
from .models import SchuelerProfile

@receiver(post_save, sender=SiteUser)
def create_schuelerProfile(sender, instance, created, **kwargs):
    if created:
        SchuelerProfile.objects.create(user=instance)