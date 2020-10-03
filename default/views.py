from django.shortcuts import render_to_response
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse
from chartit import DataPool, Chart
from registration.models import *
from django.db.models import Sum, Count
from .models import College
from xlsxwriter.workbook import Workbook
import io
from urllib.request import urlopen
# Create your views here.

@user_passes_test(lambda u: u.is_superuser, login_url='/reg/login/')
def statistics(request):

    moneyByGenralReg=Candidate.objects.aggregate(Sum('feePayable'))['feePayable__sum']
    moneyByEventReg=EventRegistration.objects.aggregate(Sum('feePayable'))['feePayable__sum'] 
    totalMoney=moneyByEventReg+moneyByGenralReg if moneyByEventReg is not None and moneyByGenralReg is not None else 0
    # print(Candidate.objects.all().values('college').annotate(college_count= Count('college')))
    # print(EventRegistration.objects.values('event').annotate(fee=Sum('feePayable'), count=Count('event'))
    # print (EventRegistration.objects.values('registeredBy__username').annotate(money=Sum('feePayable')))
    # print(Candidate.objects.values('registeredBy__username').annotate(money=Sum('feePayable')))

    ds0=DataPool(
        series=[
            {'options':{
                'source':Candidate.objects.all().values('college').annotate(college_count= Count('college'))
            },
                'terms':['college',
                         'college_count']

            }
        ]
    )

    ds=DataPool(
        series=[
            {'options':{
                'source':EventRegistration.objects.values('event').annotate(fee=Sum('feePayable'), count=Count('event'))
            },
                'terms':['event',
                         'fee',
                         'count']

            }
        ]
    )

    ds1=DataPool(
        series=[
            {
                'options':{
                    'source':EventRegistration.objects.values('registeredBy__username').annotate(money=Sum('feePayable'))
                },
                'terms':['registeredBy__username',
                         'money']
            },

        ]
    )
    ds4=DataPool(
        series=[
            {
                'options':{
                    'source':Candidate.objects.values('registeredBy__username').annotate(money=Sum('feePayable'))
                },
                'terms':['registeredBy__username',
                         'money']
            },

        ]
    )


    cht0= Chart(
        datasource=ds1,
        series_options=[{'options': {
            'type': 'column',
            'stacking': True},
            'terms': {
                'registeredBy__username': [
                    'money'],

            }}],
        chart_options={'title': {
            'text': 'Event Registration'},
            'xAxis': {
                'title': {
                    'text': 'Member'}}}
    )
    cht4= Chart(
        datasource=ds4,
        series_options=[{'options': {
            'type': 'column',
            'stacking': True},
            'terms': {
                'registeredBy__username': [
                    'money'],

            }}],
        chart_options={'title': {
            'text': 'General Registration'},
            'xAxis': {
                'title': {
                    'text': 'Member'}}}
    )

    def EventName(id):
        return Event.objects.get(pk=id).name

    def CollegeName(id):
        return College.objects.get(pk=id).name
    cht= Chart(
        datasource=ds,
        series_options=[
            {
                'options':{
                    'type':'pie',
                    'stacking':False},
                'terms':{
                    'event':[
                        'fee'
                    ]
                }
            }
        ],
        chart_options=
        {'title': {
            'text': 'Event BreakDown By Money'},
            'xAxis': {
                'title': {
                    'text': 'Event'}}},
        x_sortf_mapf_mts=(None, EventName, False )

    )

    cht2= Chart(
        datasource=ds,
        series_options=[
            {
                'options':{
                    'type':'pie',
                    'stacking':False},
                'terms':{
                    'event':[
                        'count'
                    ]
                }
            }
        ],
        chart_options=
        {'title': {
            'text': 'Event BreakDown By Number of Teams Participated'},
            'xAxis': {
                'title': {
                    'text': 'Event'}}},
        x_sortf_mapf_mts=(None, EventName, False )

    )

    cht3= Chart(
        datasource=ds0,
        series_options=[
            {
                'options':{
                    'type':'pie',
                    'stacking':False},
                'terms':{
                    'college':[
                        'college_count'
                    ]
                }
            }
        ],
        chart_options=
        {'title': {
            'text': 'College Distribution'},
            'xAxis': {
                'title': {
                    'text': 'College'}}},
        x_sortf_mapf_mts=(None, CollegeName, False )

    )

    return render_to_response('charts.html', {'user': request.user.username,'charts':[cht0,cht,cht2,cht3,cht4],'genregmoney':moneyByGenralReg, 'eventregmoney':moneyByEventReg, 'totalmoney':totalMoney})

def export(request):
    output = io.BytesIO()
    book = Workbook(output)
    sheet=book.add_worksheet('List')
    sheet.set_header("TechTrix2017 General Registration\n")
    sheet.write(0, 0, 'Id')
    sheet.write(0, 0 + 1, 'Name')
    sheet.write(0, 0 + 2, 'Email')
    sheet.write(0, 0 + 3, 'Contact Number')
    sheet.write(0, 0 + 4, 'College')

    row = 1
    column =0
    participants=Candidate.objects.all()

    for items in participants:
        sheet.write(row, column, items.id)
        sheet.write(row, column+1, items.name)
        sheet.write(row, column+2, items.email)
        sheet.write(row, column+3, items.contactNo)
        sheet.write(row, column+4,items.college.name)
        row=row+1
    book.close()

    output.seek(0)
    response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = "attachment; filename=general.xlsx"
    return response

def exportEventReg(request):
    output = io.BytesIO()
    book = Workbook(output)
    sheet=book.add_worksheet('List')
    sheet.set_header("TechTrix2017 Event Registration\n")
    sheet.write(0, 0, 'Id')
    sheet.write(0, 0 + 1, 'event')
    sheet.write(0, 0 + 2, 'Name and Number')

    row = 1
    column =0
    participants=EventRegistration.objects.all()

    for items in participants:

        participant_name_and_number=''
        member=items.participants.all()

        for members in member:
            participant_name_and_number=participant_name_and_number+' '+members.name+' ( '+members.contactNo+' ), '

        sheet.write(row, column, items.id)
        sheet.write(row, column+1, items.event.name)
        sheet.write(row, column+2, participant_name_and_number)
        row=row+1
    book.close()

    output.seek(0)
    response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = "attachment; filename=general.xlsx"
    return response