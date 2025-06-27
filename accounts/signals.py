# accounts/signals.py
import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile

logger = logging.getLogger(__name__)

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    logger.info(f"Signal triggered for User: {instance.username}, Created: {created}")
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
