from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    url(r'^login/$', views.login_user, name='login'),
    url(r'^forgotpassword/$', views.forgotpassword, name='forgotpassword'),
    url(r'^login_manager/$', views.login_user, name='login_manager'),
    url(r'logout/$', views.logout_user, name='logout_user'),
    url(r'^register/$', views.register, name='register'),
    url(r'^time/$', views.register, name='time_list'),
    url(r'^dashboard/$', views.show_dashboard, name='dashboard'),


    url(r'expenses/$', views.expenses, name='expenses'),
    url(r'^paycheck/$', views.paycheck, name='paycheck'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^dashboardemployee/$', views.dashboardemployee, name='dashboardemployee'),
    url(r'^dashboardmanager/$', views.dashboardmanager, name='dashboardmanager'),
    url(r'^dashboardhr/$', views.dashboardhr, name='dashboardhr'),
    url(r'^pto/$', views.pto, name='pto'),
    url(r'^reports/$', views.reports, name='reports'),
    url(r'^timesheets/$', views.timesheets, name='timesheets'),
    url(r'^manageaccount/$', views.manageaccount, name='manageaccount'),
    url(r'^approvalspto/$', views.approvalspto, name='approvalspto'),
    url(r'^approvalsexpenses/$', views.approvalsexpenses, name='approvalsexpenses'),
    url(r'^approvalstimesheets/$', views.approvalstimesheets, name='approvalstimesheets'),

]
