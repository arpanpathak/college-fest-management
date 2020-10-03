from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse, Http404
from django.contrib import messages
from django.urls import reverse
from  ast import literal_eval
from .forms import *
from django.db.models import Sum
from django.contrib.staticfiles.templatetags.staticfiles import static
from eventman.models import Event as EventList
from xlsxwriter.workbook import Workbook
import io
from urllib.request import urlopen
# Create your views here.

# Home page for candidate registration(General & event)
@login_required(login_url='/reg/login/')


# utility function to calculate money earned by loggedin user...
def calculate_money(request):
    moneyEarnedbyEvent=EventRegistration.objects.filter(registeredBy=request.user, feePaid=True).aggregate(Sum('feePayable'))['feePayable__sum']
    moneyEarnedbyEvent=moneyEarnedbyEvent if moneyEarnedbyEvent is not None else 0
    moneyEarnedbyGen=Candidate.objects.filter(registeredBy=request.user, feePaid=True).aggregate(Sum('feePayable'))['feePayable__sum']
    moneyEarnedbyGen = moneyEarnedbyGen if moneyEarnedbyGen is not None else 0
    moneyEarned=moneyEarnedbyEvent+moneyEarnedbyGen
    moneyEarned=moneyEarned if moneyEarned is not None else 0
    return moneyEarned

@login_required(login_url='/reg/login/')
def registrationHome(request):
    eventList=Event.objects.all()

    contexts={'eventsubmission':eventList}
    return render(request, template_name='home.html',context=contexts)


# Renders login page and also handles login request only for registrar
def loginUser(request):
    redirectTo = ""

    if request.GET:
        redirectTo = request.GET['next']

    # if request.user.is_authenticated():
    #     return HttpResponseRedirect(reverse('registration:home'))

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                if redirectTo=="":
                    return HttpResponseRedirect(reverse('registration:home'))
                else:
                    # If login page is opened due to failed authentication
                        return HttpResponseRedirect(redirectTo)

            else:
                return render(request, 'login.html', {'error_message': 'Your account has been disabled', 'next':redirectTo})
        else:
            return render(request, 'login.html', {'error_message': 'Invalid login', 'next':redirectTo})

    return render(request, template_name='login.html',context={'next':redirectTo})

@login_required(login_url='/reg/login/')
# @user_passes_test(login_url='/reg/login/', test_func= lambda user: 'registrar' in [i.name for i in user.groups.all()])
def registerForEvent(request):
    form = EventRegistrationForm(request.POST or None)

    # Calculate money by the user
    # moneyEarned =0
    moneyEarnedbyEvent=EventRegistration.objects.filter(registeredBy=request.user, feePaid=True).aggregate(Sum('feePayable'))['feePayable__sum']
    moneyEarnedbyEvent=moneyEarnedbyEvent if moneyEarnedbyEvent is not None else 0
    moneyEarnedbyGen=Candidate.objects.filter(registeredBy=request.user, feePaid=True).aggregate(Sum('feePayable'))['feePayable__sum']
    moneyEarnedbyGen = moneyEarnedbyGen if moneyEarnedbyGen is not None else 0
    moneyEarned=moneyEarnedbyEvent+moneyEarnedbyGen
    moneyEarned=moneyEarned if moneyEarned is not None else 0

    if form.is_valid():
        registration =form.save(commit=False)
        registration.registeredBy = request.user
        registration.feePayable = registration.event.fee
        registration.save()
        form.save_m2m()

        contexts = {'user': request.user.username, 'money': moneyEarned, 'registratinid':registration.pk, 'registeredevent':registration.event.name, 'regfee': registration.feePayable, 'backurl':reverse('registration:eventreg')}
        messages.add_message(request,messages.INFO,contexts)
        return HttpResponseRedirect(reverse('registration:evenregticket'))
        # return render(request, template_name='eventregtikcet.html', context=contexts)
    contexts = {'form': form, 'user': request.user.username, 'money': moneyEarned}
    return render(request, template_name='eventreg.html',context=contexts)


@login_required(login_url='/reg/login/')
# @user_passes_test(login_url='/reg/login/', test_func= lambda user: 'registrar' in [i.name for i in user.groups.all()])
def generalRegistration(request):
    form = GeneralRegistrationForm(request.POST or None)

    # Calculate money by the user
    # moneyEarned =0
    moneyEarnedbyEvent=EventRegistration.objects.filter(registeredBy=request.user, feePaid=True).aggregate(Sum('feePayable'))['feePayable__sum']
    moneyEarnedbyEvent=moneyEarnedbyEvent if moneyEarnedbyEvent is not None else 0
    moneyEarnedbyGen=Candidate.objects.filter(registeredBy=request.user, feePaid=True).aggregate(Sum('feePayable'))['feePayable__sum']
    moneyEarnedbyGen = moneyEarnedbyGen if moneyEarnedbyGen is not None else 0
    moneyEarned=moneyEarnedbyEvent+moneyEarnedbyGen

    #Check form data
    if form.is_valid():
        registration =form.save(commit=False)
        registration.registeredBy = request.user
        registration.save()
        contexts = {'user': request.user.username, 'money': moneyEarned, 'registratinid':registration.pk, 'registeredevent':"General Registration", 'regfee': registration.feePayable, 'backurl': reverse('registration:generalreg')}
        messages.add_message(request,messages.INFO,contexts)
        return HttpResponseRedirect(reverse('registration:evenregticket'))
        # return render(request, template_name='eventregtikcet.html', context=contexts)
    contexts = {'form': form, 'user': request.user.username, 'money': moneyEarned, 'fee':GENERAL_REGISTRATION_FEE}
    return render(request, template_name='generalreg.html',context=contexts)

# Score submission view
@login_required(login_url='/reg/login/')
@user_passes_test(login_url='/reg/login/', test_func= lambda user: 'coordinator' in [i.name for i in user.groups.all()] or user.is_superuser )
def scoreSub(request, event_id):
    event=get_object_or_404(EventList, pk=event_id)
    eventName=event.name
    form = EventParticipationForm(request.POST or None, eventId=event)

    #Check form data
    if form.is_valid():
        result =form.save(commit=False)
        result.scoreSubmittedBy = request.user
        result.save()
        return render(request, template_name='scoresubmisiion.html', context={'form':form,'eventName':eventName,'user':request.user.username,'event':event_id, 'message':'Score Recorded, Submit Another'})
    contexts = {'form': form, 'eventName':eventName,'user': request.user.username, 'event':event_id}
    return render(request, template_name='scoresubmisiion.html',context=contexts)

@login_required(login_url='/reg/login/')
@user_passes_test(login_url='/reg/login/', test_func= lambda user: 'coordinator' in [i.name for i in user.groups.all()] or user.is_superuser)
def leaderBoard(request, event_id):
    event=get_object_or_404(EventList, pk=event_id)
    eventName=event.name
    resultset=EventResult.objects.filter(team__event=event)
    table=LeaderBoardTable(resultset)
    contexts = {'eventName':eventName,'user': request.user.username,'event':event_id, 'table':table }
    return render(request, template_name='leaderboard.html',context=contexts)


@login_required(login_url='/reg/login/')
@user_passes_test(login_url='/reg/login/', test_func= lambda user: 'coordinator' in [i.name for i in user.groups.all()] or user.is_superuser)
def participantList(request, event_id):
    event=get_object_or_404(EventList, pk=event_id)
    eventName=event.name
    participants = EventRegistration.objects.filter(event=event, eventresult__isnull=True)
    output = io.BytesIO()
    book = Workbook(output)
    sheet=book.add_worksheet('List')
    sheet.set_header("TechTrix2017\n"+eventName)

    sheet.write(0, 0, 'Id')
    sheet.write(0, 0 + 1, 'Team Name')
    sheet.write(0, 0 + 2, 'Participant Details')
    sheet.write(0, 0 + 3, 'Score/Signature')

    row = 1
    column =0

    for items in participants:

        participant_name_and_number=''
        member=items.participants.all()

        for members in member:
            participant_name_and_number=participant_name_and_number+' '+members.name+'('+members.contactNo+'), '
        sheet.write(row, column, items.id)
        sheet.write(row, column+1, items.teamName)
        sheet.write(row, column+2, participant_name_and_number)
        sheet.write(row, column+3,'')
        row=row+1
    book.close()

    output.seek(0)
    response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = "attachment; filename="+eventName+".xlsx"
    return response

@login_required(login_url='/reg/login/')
@user_passes_test(login_url='/reg/login/', test_func= lambda user: 'registrar' in [i.name for i in user.groups.all()] or user.is_superuser)
def evenregticket(request):
    storage=messages.get_messages(request)
    contexts=None
    for message in storage:
        contexts=message
        break
    jsonstring=str(contexts)
    contexts=literal_eval(jsonstring)
    # return HttpResponse(context)
    return render(request, template_name='eventregtikcet.html', context=contexts)


# APIs ....
''''''
def verifyCandidate(request):
    """
    Returns candidate details
    :param request:
    :return: boolean
    """
    try:
        if request.method=='GET':
            id=request.GET.copy()
            if 'id' in id :
                userid = id['id']
                if Candidate.objects.filter(pk=userid):
                    candidate=Candidate.objects.get(pk=userid)
                    return JsonResponse({'resp':True, 'data':{'id': candidate.pk, 'name': candidate.name, 'college':candidate.college.name}}, safe=False)
        return JsonResponse(
            {'resp': False, 'data': None},
            safe=False)
    except:
        return JsonResponse(
            {'resp': False, 'data': None},
            safe=False)


def cadindateDetailsofEvent(request):
    """
    Returns candidate details
    :param request:
    :return: boolean
    """
    try:
        if request.method=='GET':
            id=request.GET.copy()
            if 'id' in id :
                eventRegistrationId = id['id']
                if EventRegistration.objects.filter(pk=eventRegistrationId):

                    eventRegistration=EventRegistration.objects.get(pk=eventRegistrationId)
                    htmlTable=''
                    # print((eventRegistration.participants.all()))
                    for candidate in eventRegistration.participants.all():

                        htmlTable=htmlTable+'<tr><td>'+str(candidate.name)+'</td><td>'+str(candidate.college)+'</td></tr>'
                    return JsonResponse({'resp':True, 'data':{'id': candidate.pk, 'table': htmlTable}}, safe=False)
        return JsonResponse(
            {'resp': False, 'data': None},
            safe=False)
    except:
        return JsonResponse(
            {'resp': False, 'data': None},
            safe=False)

@login_required(login_url="/reg/login")
def listregistrations(request):
    c=Candidate.objects.all()

    return render(request,'listregistrations.html',context={ 'money': calculate_money(request),'registrations': c })

@login_required(login_url="/reg/login")
def eventreglist(request):
    return render(request,'eventreglist.html',context={'money': calculate_money(request),'registrations': EventRegistration.objects.all() })
@login_required(login_url="/reg/login")
def print_slip(request):
    id=request.GET.get('id','')
    type=request.GET.get('type','')
    money=calculate_money(request)
    context={ 'money' : money }
    if(type=='g'):
        context={ type:True,'id': id, 'fields': Candidate.objects.filter(id=id).first(), 'money':money }
    elif (type=='e'):
        context= { type: True, 'id':id, 'fields': EventRegistration.objects.filter(id=id).first(), 'money':money}

    return render(request,'registrationslip.html',context=context)


def logoutUser(request):
    logout(request)
    return HttpResponseRedirect(reverse('registration:login'))