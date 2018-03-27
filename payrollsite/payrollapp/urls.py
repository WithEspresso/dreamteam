from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    url(r'^login_employee/$', views.login_user, name='login_employee'),
    url(r'^login_manager/$', views.login_user, name='login_manager'),
    url(r'logout/$', views.logout_user, name='logout_user'),
    url(r'^register/$', views.register, name='register'),
    url(r'^time/$', views.register, name='time_list'),
    url(r'^dashboard/$', views.show_dashboard, name='dashboard'),
]
