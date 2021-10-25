from django.contrib import admin
from django.urls import path
from django.conf.urls import url,include
from . import register, login, views
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    url(r'^$', login.start),
    url(r'^register$', register.register),
    url(r'^login$', login.my_login),
    url(r'^(?P<nid>\w+).html$', views.go)

]