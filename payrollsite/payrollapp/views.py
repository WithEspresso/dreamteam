from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.http import HttpResponseRedirect

from .forms import LoginForm
from .forms import UserForm
from .forms import PaidTimeOffForm
from .forms import ExpenseRequestForm

# TODO: only import models we are utilizing, let me be lazy right now please.
from .models import *

# Note, possibly convert these views from function based views to class based views in the future.


def login_user(request):
    """
    Logs in a user if a post request is given or redirects the user
    :param request:
    :return: The dashboard page for the user if the login is successful
    """
    form = LoginForm(request.POST or None)
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return render(request, 'dashboard-employee.html')
            else:
                return render(request, 'login.html', {'error_message': 'You have been banned.'})
        else:
            return render(request, 'login.html', {'error_message': 'Invalid login'})
    context = {
         "form": form,
    }
    return render(request, 'login.html', context)


def logout_user(request):
    """
    Logs a user out and redirects them to the index page.
    :param request:
    :return The index page.
    """
    logout(request)
    return redirect(login)


def reset_password(request):
    """
    Sends an email to the user to reset their password
    TODO: Use Django built in password resetting functionality versus inventing the wheel
    :param request:
    :return The password reset page.
    """
    logout(request)
    return redirect(login)


def register(request):
    """
    TODO: Add decorator so this is an HR only view
    TODO: HTTP GET, display form
    TODO: HTTP POST, validate form and add user to the database.
    Registers a user to the payroll system.
    :param request:
    :return: A success page if the User was successfully added to the system.
    """
    template_name = 'register.html'
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return render(request, 'dashboard')
    context = {
        "form": form,
    }
    return render(request, template_name, context)


def view_paycheck_information(request):
    """
    Loads a list of paychecks for the given logged in user.
    # TODO: HTTP GET, retrieve User paid time off requests as context.
    # TODO: HTTP GET, retrieve paycheck information for the given time period.
    :param   request as an http request
    :return: A rendered html page for the index with detailed paycheck information.
    """
    return render(request)


def show_dashboard(request):
    """
    TODO: Implement retrieval of User information from the database to create context to render page.
    :param   request as an http request
    :return: A rendered html page for the index with a list of current pending and process PTO requests.
    """
    return render(request, 'dashboard.html')


def paid_time_off(request):
    """
    Loads a list of paid time off requests for the user.
    Provides a form for the user to add additional PTO.
    :param   request as an http request
    :return: A rendered html page for the index with a list of current pending and process PTO requests.
    """
    form = PaidTimeOffForm(request.POST or None)
    # Retrieving existing pto requests from the database
    # Saving the form data and saving to the database.
    if request.user.is_authenticated:
        this_username = request.user
        user = User.objects.get(username=this_username)
        pto_requests = PaidTimeOffRequests.objects.filter(user_id__username=this_username)
        if form.is_valid():
            pto_request = form.save(commit=False)
            pto_request.user_id = user
            pto_request.status = 'Pending'
            pto_request.save()
            return HttpResponseRedirect('pto/')
    else:
        return render(request, 'login.html')
    context = {
        "form": form,
        "pto_requests": pto_requests
    }
    return render(request, 'pto.html', context)


def approve_paid_time_off(request):
    """
    Loads a list of pending paid time off requests.
    TODO: Add decorator so this is a manager only view.
    TODO: HTTP GET, retrieve pending pto request. Implement manager only access to this view. Redirect if failed.
    TODO: HTTP POST, update status of PTO requests.
    :param   request as an http request
    :return: A rendered html page for the index with a list of current pending and process PTO requests.
    """
    return render(request)


def expense_reimbursement(request):
    """
    Loads a list of expense reimbursement requests for the user.
    # TODO: HTTP GET, retrieve User paid time off requests as context.
    # TODO: HTTP POST, update table with expense reimbursement request for current user.
    :param   request as an http request
    :return: A rendered html page for the index with a list of current pending and expense reimbursement requests.
    """
    form = ExpenseRequestForm(request.POST or None)
    # Retrieving existing pto requests from the database
    # Saving the form data and saving to the database.
    if request.user.is_authenticated:
        this_username = request.user
        user = User.objects.get(username=this_username)
        expense_requests = ExpenseRequest.objects.filter(user_id__username=this_username)
        if form.is_valid():
            expense_request = form.save(commit=False)
            expense_request.user_id = user
            expense_request.status = 'Pending'
            expense_request.save()
            # Redirect is done instead of rendering because refreshing will cause form resubmission.
            return HttpResponseRedirect('expenses/')
    else:
        return render(request, 'login.html')
    context = {
        "form": form,
        "expense_requests": expense_requests,
    }
    return render(request, 'expenses.html', context)


def approve_expense_reimbursement(request):
    """
    Loads a list of pending expense reimbursement requests.
    TODO: Add decorator so this is a manager only view.
    TODO: HTTP GET, retrieve pending pto request. Implement manager only access to this view. Redirect if failed.
    TODO: HTTP POST, update status of PTO requests.
    :param   request as an http request
    :return: A rendered html page for the index with a list of current pending and process PTO requests.
    """
    return render(request)


def display_time_sheet(request):
    """
    Displays a form so the user can input their time sheet information
    TODO: HTTP NONE, display time sheet form.
    TODO: HTTP POST, validate time and add to the database.
    :param   request as an http request
    :return: A rendered html page for inputting time sheet requests
    """
    return render(request)


def approve_time_sheet(request):
    """
    Loads a list of pending time sheets from employees, managers, and HR
    TODO: Add decorator so this is a manager only view.
    TODO: HTTP NONE, display time sheet form.
    TODO: HTTP GET, retrieve pending pto request. Implement manager only access to this view. Redirect if failed.
    TODO: HTTP POST, update status of PTO requests.
    :param   request as an http request
    :return: A rendered html page for the index with a list of current pending and process PTO requests.
    """
    return render(request)


def generate_reports(request):
    """
    Displays reports about the manager's employees.
    TODO: Add decorator so this is a manager only view.
    TODO: HTTP NONE, display time sheet form.
    TODO: HTTP GET, display reports about a given user by filtering results.
    :param   request as an http request
    :return: A rendered html page with the employee reports.
    """
    return render(request)


def view_personal_information(request):
    """
    Displays personal information to the user.
    TODO: HTTP NONE, display personal information.
    :param   request as an http request
    :return: A rendered html page with user information.
    """
    return render(request)


def update_personal_information(request):
    """
    Allows HR to search for user information and edit it.
    TODO: Add a decorator so that it is an HR only view
    TODO: HTTP NONE, display personal information.
    TODO: HTTP GET, display personal information of the given user_id.
    TODO: HTTP POST, update personal information
    :param   request as an http request
    :return: A rendered html page with user information.
    """
    return render(request)


def manage_wages(request):
    """
    Allows HR to manage wages of a given employee
    TODO: Add a decorator so that it is an HR only view
    TODO: HTTP NONE, displays form to search for an employee
    TODO: HTTP GET, display wage information of the given user_id.
    TODO: HTTP POST, update wage information
    :param   request as an http request
    :return: A rendered html page with wage information
    """
    return render(request)