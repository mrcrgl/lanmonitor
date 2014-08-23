from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import TargetHost
from .tasks import enrich_target_host

@receiver(signal=post_save, sender=TargetHost)
def enrich_target_host(sender, instance, created, **kwargs):

    if created:
        enrich_target_host.delay(instance)