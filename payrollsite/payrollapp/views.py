from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout

from .models import TimeRecord
from .forms import LoginForm
from .forms import UserForm

# Create your views here.


# Loads the index page
# @param:   An http request
# @return:  A rendered html page for the index.
def index(request):
    return render(request, 'index.html', context={})


def forgotpassword(request):
    return render(request, 'forgotpassword.html', context={})


# Logs in a user if a post request is given or redirects the user
# to the login page.
# @param:   An http request
# @return:  The profile page for the user if the login is successful
def login_user(request):
    form = LoginForm(request.POST or None)
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect(show_dashboard)
            else:
                return render(request, 'login.html', {'error_message': 'You have been banned.'})
        else:
            return render(request, 'login.html', {'error_message': 'Invalid login'})
    context = {
         "form": form,
    }
    return render(request, 'login.html', context)


# Logs a user out.
def logout_user(request):
    logout(request)
    return redirect(index)


def register(request):
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


# Loads a list of clock in and clock out times for that user.
# @param:   An http request
# @return:  A rendered html page for the index with a list of all previous clock in/out times.
def show_dashboard(request):
    return render(request, 'dashboard.html')


# Loads a list of clock in and clock out times for that user.
# @param:   An http request
# @return:  A rendered html page for the index with a list of all previous clock in/out times.
def time_list(request):
    all_posts = TimeRecord.objects.all()
    context = {'all_times': all_posts}
    return render(request, 'payrollApp/time_records_list.html', context)


def expenses(request):
    return render(request, 'expenses.html', context={})


def paycheck(request):
    return render(request, 'paycheck.html', context={})


def signup(request):
    return render(request, 'signup.html', context={})


def dashboardemployee(request):
    return render(request, 'dashboard-employee.html', context={})


def dashboardmanager(request):
    return render(request, 'dashboard-manager.html', context={})


def dashboardhr(request):
    return render(request, 'dashboard-hr.html', context={})


def pto(request):
    return render(request, 'pto.html', context={})


def reports(request):
    return render(request, 'reports.html', context={})


def timesheets(request):
    return render(request, 'timesheets.html', context={})

def manageaccount(request):
    return render(request, 'manageaccount.html', context={})
