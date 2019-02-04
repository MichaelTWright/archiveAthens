from django.conf.urls import url
from . import views  

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^archive_create$', views.archive_create),
    url(r'^favorited/(?P<id>\d+)$', views.favorited),
    url(r'^favorites$', views.favorites),
    url(r'^delete/(?P<id>\d+)$', views.delete),
    url(r'^unlike/(?P<id>\d+)$', views.unlike),
    url(r'^uploads/(?P<id>\d+)$', views.uploads),
    url(r'^find$', views.find),
]      




