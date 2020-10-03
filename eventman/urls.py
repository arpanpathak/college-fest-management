from django.conf.urls import url
from . import views

app_name='eventapp'

urlpatterns = [
    url(r'^eventDet/(?P<event_id>[0-9]+)', views.eventDet, name='eventDet')
     # url(r'^event', views.registrationHome, name='home'),
    # url(r'^$', views.registrationHome, name='home'),
    # url(r'^login/', views.loginUser, name='login'),
    # url(r'^candidate/', views.verifyCandidate, name='user')
]