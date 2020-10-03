from django.http import HttpResponse, JsonResponse
from .models import Event
# Create your views here.

def eventDet(request, event_id):
    try:
        print('hello')
        if Event.objects.filter(pk=event_id):
            event=Event.objects.get(pk=event_id)
            print('hello again')
            return JsonResponse({'resp':True, 'data':{'id': event.pk, 'name': event.name, 'fees':event.fee, 'minParticipant':event.minParticipant, 'maxParticipant': event.maxParticipant}}, safe=False)
        return JsonResponse(
            {'resp': False, 'data': None},
            safe=False)
    except:
        return JsonResponse(
            {'resp': False, 'data': None},
            safe=False)