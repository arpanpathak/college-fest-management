from django import forms
from .models import *
import django_tables2 as table
from django.core.exceptions import ValidationError

class EventRegistrationForm(forms.ModelForm):
    participants = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'off', 'data-role':'tagsinput'}),required=True)

    class Meta:
        model=EventRegistration
        fields=['event', 'participants', 'teamName', 'feePaid']

    def clean_feePaid(self):
        feepaid=self.cleaned_data.get('feePaid')
        if not feepaid:
            raise ValidationError('Please pay the fee First :)')
        return feepaid

    def clean_participants(self):
        participants_data = self.cleaned_data.get('participants')
        event = self.cleaned_data.get('event')
        participants =[]
        for pd in participants_data.split(','):
            p = Candidate.objects.get(pk=pd)
            participants.append(p)
        if not (event.minParticipant <= len(participants) <= event.maxParticipant):
            raise ValidationError('Number of Participants exceeded :D')
        return participants

    def __init__(self, *args, **kwargs):
        super(EventRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['event'].empty_label = ''
        # following line needed to refresh widget copy of choice list
        self.fields['event'].widget.choices =self.fields['event'].choices


class GeneralRegistrationForm(forms.ModelForm):
    others = forms.CharField(required=False)
    class Meta:
        model=Candidate
        fields=['name', 'email', 'contactNo', 'college','others', 'refferedBy','feePaid']

    def clean_feePaid(self):
        feepaid=self.cleaned_data.get('feePaid')
        if not feepaid:
            raise ValidationError('Please pay the fee First :)')
        return feepaid

    def clean_college(self):
        colName=self.cleaned_data.get('college')
        if colName.name=='Other':
            try:
                newName = College(name=self.data['others'])
                newName.save()
                return newName
            except:
                raise ValidationError('College is already in list. If not appearing refresh the page')
        return colName

    def __init__(self, *args, **kwargs):
        super(GeneralRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['college'].empty_label = ''

        # self.fields['college'].choices = list(self.fields['college'].choices

class EventParticipationForm(forms.ModelForm):
    class Meta:
        model=EventResult
        fields=['team', 'score', 'participated']

    def clean_participated(self):
        pd=self.cleaned_data.get('participated')
        if not pd:
            raise ValidationError("You need to tick this")
        return pd


    def __init__(self, *args, **kwargs):
        eventId = kwargs.pop('eventId', None)
        super(EventParticipationForm, self).__init__(*args, **kwargs)

        self.fields['team'].empty_label = ''
        self.fields['team'].queryset=EventRegistration.objects.filter(feePaid=True, event=eventId, eventresult__isnull=True )

#table for view render
class LeaderBoardTable(table.Table):
    class Meta:
        model=EventResult
        fields=['team','score', 'timeStamp']
        attrs={'class':'table', 'id':'leaderboard'}
        orderable=False