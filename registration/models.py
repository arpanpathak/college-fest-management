"""
Importing Django libd
"""
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from default.models import College
from eventman.models import Event
from  django.db.models.signals import pre_save

# Create your models here.

GENERAL_REGISTRATION_FEE = 20

class CampusAmbassador(models.Model):
    """ 
    Stores name of all Campus Ambassador... 
    """
    name= models.CharField(max_length=50)
    contactNo=models.CharField(max_length=10)
    college=models.ForeignKey(College,on_delete=models.PROTECT)
    def __str__(self):
        return self.name

class Candidate(models.Model):
    """
    General Registration objects will be stored in this model
    Users with group 'registrar' will be able to register the general Candidates
    """
    name = models.CharField(blank=False, null=False, max_length=50)
    email = models.EmailField(blank=False, null=False, unique=True)
    contactNo = models.CharField(blank=False, null=False, max_length=10)

    college = models.ForeignKey(College, null=False,on_delete=models.PROTECT)
    feePayable = models.IntegerField(default=GENERAL_REGISTRATION_FEE)
    feePaid = models.BooleanField(default=False, null=False)
    registeredBy = models.ForeignKey(User, limit_choices_to={'groups__name':'registrar'}, null=False,on_delete=models.PROTECT)
    refferedBy = models.ForeignKey(CampusAmbassador, null=True, blank=True,on_delete = models.PROTECT)
    timeStamp = models.DateTimeField(default=timezone.now, editable=False)
    def __str__(self):
        return str(self.pk)+"-"+self.name+"-"+str(self.college)


class EventRegistration(models.Model):
    """
    Stores the imformation of event registration
    """
    event = models.ForeignKey(Event, null=False,on_delete=models.PROTECT)
    feePayable = models.IntegerField()
    feePaid = models.BooleanField(default=False, null=False)
    participants = models.ManyToManyField(Candidate)
    teamName=models.CharField(max_length=40, null=True)
    timeStamp = models.DateTimeField(default=timezone.now, editable=False)
    registeredBy = models.ForeignKey(User, limit_choices_to={'groups__name':'registrar'}, null=False,on_delete=models.PROTECT)

    def __str__(self):
        return str(self.pk)+" "+str(self.teamName)+" "+str(self.event)

class EventResult(models.Model):
    """
    Model for storing result for events
    """
    team = models.OneToOneField(EventRegistration, null=False,on_delete=models.PROTECT)
    participated = models.BooleanField(default=False, null=False)
    score = models.DecimalField(max_digits=10, decimal_places=4, null=True)
    nextRoundEligibility = models.BooleanField(default=False, null=False)
    scoreSubmittedBy = models.ForeignKey(User, limit_choices_to={'groups__name':'coordinator'}, null=False,on_delete=models.PROTECT)
    timeStamp = models.DateTimeField(default=timezone.now, editable=False)
    def __str__(self):
        return str(self.team.pk)
