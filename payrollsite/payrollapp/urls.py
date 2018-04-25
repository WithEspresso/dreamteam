from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    path('', views.login_user, name='index'),
    url(r'dashbaord/#', views.show_dashboard, name='dashboard'),
    url(r'logout/$', views.logout_user, name='logout_user'),
    url(r'paycheck/$', views.view_paycheck_information, name='paycheck'),
    url(r'timesheet/$', views.display_time_sheet, name='timesheets'),
    url(r'expense-requests/$', views.expense_reimbursement, name='expense-requests'),
    url(r'pto/$', views.paid_time_off, name='pto'),
]
