from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^associates/$', views.associates, name='associates'),
    url(r'^associates/(?P<page>[0-9]+)/$', views.associatesNext, name='associatesNext'),
    url(r'^$', views.index, name='index'),
    url(r'^associates/details/(?P<associate_id>[0-9]+)/$', views.details, name='details'),
]
