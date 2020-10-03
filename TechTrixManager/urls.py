"""TechTrixManager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from default import views as defaultview

admin.site.site_header="TECHTRIX 18"

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('registration.urls'),name='root'),
    url(r'^reg/', include('registration.urls')),
    url(r'^event/', include('eventman.urls')),
    url(r'^status/', defaultview.statistics, name='status'),
    url(r'^export/', defaultview.export, name='export'),
    url(r'^exportEvent/', defaultview.exportEventReg, name='exportEvent')
]
