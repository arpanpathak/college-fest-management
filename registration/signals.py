from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import EventRegistration
from .models import EventResult


# @receiver(post_save, sender=EventRegistration)
# def createEventResultObject(sender, instance, created, **kwargs):
#     if created:
#         EventResult.objects.create(team=instance)
#
