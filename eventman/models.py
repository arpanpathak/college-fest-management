from django.db import models
# Create your models here.


class Event(models.Model):
    """
    Model for storing different types of events
    """
    name = models.CharField(blank=False, null=False, max_length=50)
    minParticipant = models.IntegerField(null=False)
    maxParticipant = models.IntegerField(null=False)
    fee = models.IntegerField(null=False, blank=False, default=0)
    def __str__(self):
        return self.name

