from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    path('', views.login_user, name='index'),
    url(r'logout/$', views.logout_user, name='logout_user'),
    url(r'paycheck/$', views.logout_user, name='paycheck'),
    url(r'timesheet/$', views.logout_user, name='timesheets'),
    url(r'expenses/$', views.expense_reimbursement, name='expenses'),
    url(r'pto/$', views.paid_time_off, name='pto'),
]
