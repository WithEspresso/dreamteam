from django.conf.urls import url
from django.urls import path
from django.contrib.auth.views import login, logout

from . import views

urlpatterns = [
    # Unauthenticated users only
    path('', views.login_user, name='index'),
    url(r'logout/$', views.logout_user, name='logout'),

    # All user groups
    url(r'dashboard/', views.show_dashboard, name='dashboard'),

    # Employee only
    url(r'logout/$', views.logout_user, name='logout_user'),
    url(r'paycheck/$', views.view_paycheck_information, name='paycheck'),
    url(r'timesheet/$', views.display_time_sheet, name='timesheets'),
    url(r'expense-requests/$', views.expense_reimbursement, name='expense-requests'),
    url(r'pto/$', views.paid_time_off, name='pto'),

    # Manager only
    url(r'reports/$', views.generate_reports, name='reports'),
    url(r'timesheet-approvals/$', views.approve_time_sheet, name='timesheet-approvals'),
    url(r'expense-approvals/$', views.approve_expense_reimbursement, name='expense-approvals'),
    url(r'pto-approvals/$', views.approve_paid_time_off, name='pto-approvals'),

    # Human Resources only
    url(r'signup/$', views.register, name='signup'),
    url(r'manageaccounts/$', views.manage_accounts, name='manage-accounts'),
]
