from django.contrib import admin
from .models import *
from .forms import *

# Register your models here.


class EventRegistrationAdmin(admin.ModelAdmin):
    form = EventRegistrationForm

admin.site.register(Candidate)
admin.site.register(EventRegistration)
admin.site.register(EventResult)
admin.site.register(CampusAmbassador)