from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.contrib.auth.models import Group


import json

from .forms import LoginForm
from .forms import UserForm
from .forms import PaidTimeOffRequestForm
from .forms import ExpenseRequestForm
from .forms import UserMetaDataForm
from .forms import UserSignUpForm
from .forms import TimeSheetForm

# TODO: only import models we are utilizing, let me be lazy right now please.
from .models import *


def get_layout_based_on_user_group(user):
    """
    Helper function to determine which html base page to render.
    Returns the appropriate layout depending on the user's permissions.
    :param user from request.user
    :return: a string containing the appropriate layout for th e page.
    """
    if user.groups.filter(name="HumanResources").exists():
        return "layout-hr.html"
    elif user.groups.filter(name="Manager").exists():
        return "layout-manager.html"
    else:
        return "layout-employee.html"


def check_user_group(user, group_name):
    """
    Helper function to determine permissions.
    Checks to see if a user is part of a group.
    :param user from request.user
    :param group_name to check in the form of a string
    :return: a string containing the appropriate layout for th e page.
    """
    if user.groups.filter(name=group_name).exists():
        return True
    return False


def login_user(request):
    """
    Available to anonymous and registered users.
    Logs in a user if a post request is given or redirects the user
    :param request:
    :return: The dashboard page for the user if the login is successful
    """
    user_meta_data_form = UserMetaDataForm(request.POST or None)
    user_form = UserSignUpForm(request.POST or None)

    # Behavior for registering a new user.
    if request.method == "POST" and user_form.is_valid() and user_meta_data_form.is_valid():
        # Check django.auth.contrib's user form, register the user.
        user = user_form.save(commit=False)
        username = user_form.cleaned_data['username']
        password = user_form.cleaned_data['password']
        user.set_password(password)
        user.save()
        # Now, get our metadata and add it to the table.
        user_metadata = user_meta_data_form.save(commit=False)
        user_metadata.user_id = user
        user_metadata.address = user_meta_data_form.cleaned_data['address']
        user_metadata.social_security_number = user_meta_data_form.cleaned_data['social_security_number']
        user_metadata.group = user_meta_data_form.cleaned_data['group']
        user_metadata.company = user_meta_data_form.cleaned_data['company']
        # Save the new tables if both forms are okay.
        user_metadata.save()
        # Add the user to their appropriate group.
        my_group = Group.objects.get(name=user_metadata.group)
        my_group.user_set.add(user)
        # Create PTO hours for the user.
        pto_hours = PaidTimeOffHours()
        pto_hours.user_id = user
        pto_hours.save()
        # Now login the user.
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('dashboard')

    # Behavior for logging in.
    form = LoginForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('dashboard')
            else:
                return render(request, 'login.html', {'error_message': 'You have been banned.'})
        else:
            return render(request, 'login.html', {'form': form, 'error_message': 'Invalid login'})

    context = {
        "form": form,
        "user_meta_data_form": user_meta_data_form,
        "user_form": user_form
    }
    return render(request, 'login.html', context)


def logout_user(request):
    """
    Logs a user out and redirects them to the index page.
    :param request:
    :return The index page.
    """
    logout(request)
    return redirect(login_user)


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
    Registers an initial HR user to the payroll system.
    Registration should start here for a company, then
    HR can register the rest of its users.
    :param request:
    :return: A success page if the User was successfully added to the system.
    """
    template_name = 'signup.html'
    message = None
    user_form = UserSignUpForm(request.POST or None)
    user_metadata_form = UserMetaDataForm(request.POST or None)
    if user_form.is_valid() and user_metadata_form.is_valid():
        # Check django.auth.contrib's user form, register the user.
        user = user_form.save(commit=False)
        username = user_form.cleaned_data['username']
        password = user_form.cleaned_data['password']
        user.set_password(password)
        user.save()
        # Now, get our metadata and add it to the table.
        user_metadata = user_metadata_form.save(commit=False)
        user_metadata.user_id = user
        user_metadata.address = user_metadata_form.cleaned_data['address']
        user_metadata.social_security_number = user_metadata_form.cleaned_data['social_security_number']
        user_metadata.group = user_metadata_form.cleaned_data['group']
        user_metadata.company = user_metadata_form.cleaned_data['company']
        # Save the new tables if both forms are okay.
        user_metadata.save()
        # Add the user to their appropriate group.
        my_group = Group.objects.get(name=user_metadata.group)
        my_group.user_set.add(user)
        # Create PTO hours for the user.
        pto_hours = PaidTimeOffHours()
        pto_hours.user_id = user
        pto_hours.save()
        # Success message
        message = "Successfully created new user: " + str(username)
        # Clear forms.
        user_form = UserSignUpForm()
        user_metadata_form = UserMetaDataForm()

    context = {
        "user_form": user_form,
        "user_metadata_form": user_metadata_form,
        "message": message
    }
    return render(request, template_name, context)


def view_paycheck_information(request):
    """
    Loads a list of paychecks for the given logged in user.
    Allows the user to search paychecks between a time range.
    :param   request as an http request
    :return: A rendered html page for the index with detailed paycheck information.
    """
    error_message = None
    # If the user is logged in, get information from the html input tags.
    if request.method == "GET" and request.user.is_authenticated:
        layout = get_layout_based_on_user_group(request.user)
        # Get start and end dates for search parameters.
        start_date = request.GET.get("start-date")
        end_date = request.GET.get("end-date")
        username = request.user
        # If the input tags have values, convert them to datetime objects and use
        # them to search the database for values within their range.
        if start_date is not None and start_date is not "" and end_date is not None and end_date is not "":
            start_date = datetime.datetime.strptime(start_date, '%m/%d/%Y')
            end_date = datetime.datetime.strptime(end_date, '%m/%d/%Y')
            results = PaycheckInformation.search_by_time_period(start_date, end_date, username)
            # Case where no values have been found.
            if len(results) == 0:
                error_message = "Sorry, no paychecks could be found within the specified time period."
        # Load the last five paychecks for the user if they are not currently filtering by time period.
        else:
            error_message = "Please input a date range in order to search for paychecks."
            results = PaycheckInformation.objects.filter(user_id__username__exact=username)
        # Calculate taxes for paychecks.
        state_tax_rate = 0.15
        city_tax_rate = 0.05
        federal_tax_rate = 0.10
        state_taxes = list()
        city_taxes = list()
        net_pay = list()
        federal_taxes = list()
        total_taxes = list()
        # TODO: Move this to a database table to save time on calculations.
        for result in results:
            amount = float(result.amount)
            state_tax = round(amount * state_tax_rate, 2)
            state_taxes.append("%.2f" % state_tax)
            city_tax = round(amount * city_tax_rate, 2)
            city_taxes.append("%.2f" % city_tax)
            federal_tax = round(amount * federal_tax_rate, 2)
            federal_taxes.append("%.2f" % federal_tax)
            total_tax = round((state_tax_rate + city_tax_rate + federal_tax_rate) * amount, 2)
            total_taxes.append("%.2f" % total_tax)
            net_pay.append("%.2f" % (round(amount - total_tax, 2)))
        zipped_data = zip(results, state_taxes, city_taxes, federal_taxes, total_taxes, net_pay)

        context = {
            'layout': layout,
            'results': results,
            'error_message': error_message,
            'tax_information': zipped_data
        }
    # User is not logged in. Redirecting to the login page with an error message.
    else:
        return redirect(login_user)
    return render(request, 'paycheck.html', context)


def show_dashboard(request):
    """
    :param   request as an http request
    :return: A rendered html page with the user's dashboard.
    """
    if request.user.is_authenticated:
        layout = get_layout_based_on_user_group(request.user)
        context = {
            "layout": layout
        }
        return render(request, 'dashboard.html', context)
    return redirect(login_user)


def paid_time_off(request):
    """
    Loads a list of paid time off requests for the user.
    Provides a form for the user to add additional PTO.
    :param   request as an http request
    :return: A rendered html page for the index with a list of current pending and process PTO requests.
    """
    error_message = ""
    form = PaidTimeOffRequestForm(request.POST or None)
    if request.user.is_authenticated:
        layout = get_layout_based_on_user_group(request.user)

        # Retrieving existing pto requests from the database
        this_username = request.user
        user = User.objects.get(username=this_username)
        pto_requests = PaidTimeOffApproval.objects.filter(user_id__username=this_username)

        # Retrieving remaining pto hours from the database
        remaining_pto = PaidTimeOffHours.objects.get(user_id__username=this_username)
        remaining_pto = remaining_pto.remaining_hours

        # Saving the form data and saving to the database if the user is sending a POST request.
        if request.method == "POST":
            # Iterate through all entries and append valid ones to a list.
            pto_entries = list()
            total_hours = 0
            for i in range(0, 5):
                pto_entry = PaidTimeOffEntry()
                pto_entry.user_id = user
                date = request.POST.get("date" + str(i))
                all_hours = request.POST.getlist('hours')
                hours = float(all_hours[i])
                if hours is not None and hours > 0 and date is not None:
                    pto_entry.date = date
                    pto_entry.hours = hours
                    total_hours += int(hours)
                    pto_entries.append(pto_entry)
            # If there are valid entries, create a new approval and link them all by foreign key.
            if pto_entries is not None and total_hours > 0:
                approval = PaidTimeOffApproval()
                approval.user_id = user
                approval.save()
                for entry in pto_entries:
                    entry.paid_time_off_approval_id = approval
                    entry.save()
                return HttpResponseRedirect('pto/')
            else:
                error_message = "Total hours cannot be zero."
        # Load the page with the context dictionary.
        context = {
            "loop_times": range(0, 5),
            "layout": layout,
            "form": form,
            "pto_approvals": pto_requests,
            "remaining_pto": remaining_pto,
            "error_message": error_message
        }
        return render(request, 'pto.html', context)
    else:
        return redirect(login_user)


def approve_paid_time_off(request):
    """
    Loads a list of pending paid time off requests.
    TODO: Add decorator so this is a manager only view.
    TODO: HTTP GET, retrieve pending pto request. Implement manager only access to this view. Redirect if failed.
    TODO: HTTP POST, update status of PTO requests.
    :param   request as an http request
    :return: A rendered html page for the index with a list of current pending and process PTO requests.
    """
    if request.user.is_authenticated and check_user_group(request.user, "Manager"):
        if request.method == "POST":
            pto_id = request.POST['pto_id']
            pto_request = PaidTimeOffApproval.objects.get(paid_time_off_approval_id=pto_id)
            if "approve" in request.POST:
                pto_request.status = "Approved"
            if "reject" in request.POST:
                pto_request.status = "Denied"
            pto_request.save()

        # Default behavior: Load all pending time sheets.
        pending_pto_requests = PaidTimeOffApproval.objects.filter(status="Pending")
        processed_pto_requests = PaidTimeOffApproval.objects.exclude(status="Pending")

        # Load all approved time sheets.
        context = {
            'pending_pto_requests': pending_pto_requests,
            'processed_pto_requests': processed_pto_requests
        }
        return render(request, 'approvalspto.html', context)
    else:
        return redirect(login_user)


def expense_reimbursement(request):
    """
    Loads a list of expense reimbursement requests for the user.
    :param   request as an http request
    :return: A rendered html page for the index with a list of current pending and expense reimbursement requests.
    """
    if request.user.is_authenticated:
        if request.POST:
            form = ExpenseRequestForm(request.POST, request.FILES)
        else:
            form = ExpenseRequestForm()
        layout = get_layout_based_on_user_group(request.user)
        # Retrieving existing  requests from the database
        this_username = request.user
        user = User.objects.get(username=this_username)
        expense_requests = Expenses.objects.filter(user_id__username=this_username)
        print("FOUND EXPENSE REQUESTS: ")
        print(expense_requests)
        # Display the page normally.
        context = {
            "layout": layout,
            "form": form,
            "expense_requests": expense_requests,
        }
        # If the user is posting, saving the form data and saving to the database.
        if form.is_valid():
            print("CREATING EXPENSE REIMBURSEMENT")
            form = ExpenseRequestForm(request.POST, request.FILES)
            new_expense_request = form.save(commit=False)
            new_expense_request.user_id = user
            new_expense_request.status = 'Pending'
            print(new_expense_request.file.url)
            new_expense_request.save()
            # Redirect is done instead of rendering because refreshing will cause form resubmission.
            return HttpResponseRedirect('expense-requests/')
        else:
            return render(request, 'expense-requests.html', context)
    else:
        # User is not logged in. Show them the way.
        return redirect(login_user)


def approve_expense_reimbursement(request):
    """
    Manager only view.
    Loads a list of pending expense reimbursement requests.
    :param   request as an http request
    :return: A rendered html page for the index with a list of current pending and process PTO requests.
    """
    if request.user.is_authenticated and check_user_group(request.user, "Manager"):
        # If the user is making a post request, updates the database.
        if request.method == "POST":
            expense_id = request.POST['expense_id']
            expense_request = Expenses.objects.get(expense_id=expense_id)
            if "approve" in request.POST:
                expense_request.status = "Approved"
            if "reject" in request.POST:
                expense_request.status = "Denied"
            expense_request.save()

        # Default behavior: Load all pending time sheets.
        pending_expense_requests = Expenses.objects.filter(status="Pending")
        processed_expense_requests = Expenses.objects.exclude(status="Pending")

        # Load all approved time sheets.
        context = {
            'pending_expense_requests': pending_expense_requests,
            'processed_expense_requests': processed_expense_requests
        }
        return render(request, 'approvalsexpenses.html', context)
    else:
        return redirect(login_user)


def display_time_sheet(request):
    """
    Displays a form so the user can input their time sheet information and view
    submitted time sheets.
    :param   request as an http request
    :return: A rendered html page for inputting time sheet requests
    """
    if request.user.is_authenticated:
        # Get the correct layout.
        user = request.user
        layout = get_layout_based_on_user_group(user)
        # Write time sheet to the database.
        if request.method == "POST":
            week1 = request.POST.get("week1")
            if week1 is not None and week1 is not "":
                time_sheet_entries = list()
                total_hours = 0
                all_hours = request.POST.getlist('hours')
                week = request.POST.get("week1")
                day = datetime.datetime.strptime(week + '-1', "%Y-W%W-%w")
                # Get all of the time sheet entries for that week.
                # If the hours submitted is greater than zero, append it to the
                # approvals we are building.
                for i in range(0, 7):
                    hours = float(all_hours[i])
                    entry = TimeSheetEntry()
                    entry.date = day
                    entry.number_hours = hours
                    entry.user_id = user
                    total_hours += hours
                    if hours > 0:
                        time_sheet_entries.append(entry)
                    day += datetime.timedelta(days=1)
                # If the total hours is greater than zero and there are valid entries,
                # Create an approval object and add the approval id to all of the entries.
                if total_hours > 0 and time_sheet_entries is not None:
                    approval = TimeSheetApprovals()
                    approval.user_id = user
                    approval.save()
                    for entry in time_sheet_entries:
                        entry.time_sheet_approvals_id = approval
                        entry.save()
                    return HttpResponseRedirect('timesheet/')
        # Get total hours for the current pay period.
        total_hours = TimeSheetEntry.calculate_pay_period_total_hours(user)
        # Get all time sheet approvals by user
        time_sheet_approvals = TimeSheetApprovals.get_all_by_username(user)
        context = {
            "loop_times": range(0, 7),
            'layout': layout,
            'total_hours': total_hours,
            'time_sheet_approvals': time_sheet_approvals
        }
    else:
        return redirect(login_user)
    # Load the page normally for an authenticated user.
    return render(request, 'timesheets.html', context)


def approve_time_sheet(request):
    """
    Manager only view.
    Loads a list of pending time sheets from employees, managers, and HR
    :param   request as an http request
    :return: A rendered html page for the index with a list of current pending and process PTO requests.
    """
    # Behavior for updating database entries
    if request.user.is_authenticated and check_user_group(request.user, "Manager"):
        # If the user is sending a post request, make changes to the database.
        if request.method == "POST":
            time_sheet_id = request.POST['time_sheet_id']
            time_sheet = TimeSheetApprovals.objects.get(time_sheet_approvals_id=time_sheet_id)
            if "approve" in request.POST:
                time_sheet.status = "Approved"
            if "reject" in request.POST:
                time_sheet.status = "Denied"
            time_sheet.save()

        # HTTP None, Default behavior: Load all pending and processed time sheets.
        pending_time_sheets = TimeSheetApprovals.objects.filter(status="Pending")
        processed_time_sheets = TimeSheetApprovals.objects.exclude(status="Pending")
        time_sheet_approvals = TimeSheetApprovals.objects.all()

        # Load all approved time sheets.
        context = {
            'time_sheet_approvals': time_sheet_approvals,
            'pending_time_sheets': pending_time_sheets,
            'processed_time_sheets': processed_time_sheets
        }
        return render(request, 'approvalstimesheets.html', context)
    else:
        return redirect(login_user)


def generate_reports(request):
    """
    Manager only view.
    Displays reports about the manager's employees.
    TODO: How does graph work pls x axis doesn't take python data structures
    :param   request as an http request
    :return: A rendered html page with the employee reports.
    """
    """
    For the #container-graph-paycheck, create a tuple of the next twelve months
    and calculate the total dollars per month. 
    """
    if request.user.is_authenticated and check_user_group(request.user, "Manager"):
        users = User.objects.all()
        last_twelve_months = PaycheckInformation.get_last_years_history()
        context = {
            'last_twelve_months': json.dumps(last_twelve_months)
        }
        return render(request, 'reports.html', context)
    else:
        return redirect(login_user)


def manage_accounts(request):
    """
    :param   request as an http request
    :return: A rendered html page with wage information
    """
    if request.user.is_authenticated and check_user_group(request.user, "HumanResources"):
        # Check for post request and process data accordingly.
        if request.method == "POST":
            # Currently not working. Will debug later.
            """
            user_id = request.POST.get("user_id")
            metadata_id = request.POST.get("metadata_id")
            user_instance = User.objects.get(username=user_id)
            metadata_instance = UserMetaData.objects.get(user_meta_data_id=metadata_id)
            metadata_form = UserMetaDataForm(request.POST, instance=metadata_instance)
            user_form = UserForm(request.POST, instance=user_instance)
            if metadata_form.is_valid() and user_form.is_valid():
                metadata_form.save()
                user_form.save()
            """

        # Gets all user metadata relevant to the company HR works for from the database.
        # TODO: Filter by company of user in instance.
        all_user_metadata = UserMetaData.objects.all().order_by('user_id__username')

        # Creates a custom form with prepopulated data for each entry for user meta data
        metadata_forms = list()
        for data in all_user_metadata:
            form = UserMetaDataForm(instance=data)
            metadata_forms.append(form)

        # Creates a custom form with prepopulated data for each entry for django.auth.contrib.models.User
        user_forms = list()
        all_users = User.objects.all().exclude(django_user_id=None).order_by('username')
        for user in all_users:
            form = UserForm(instance=user)
            user_forms.append(form)

        # Zip all data into a tuple for iterating through in template.
        zipped_data = zip(all_user_metadata, metadata_forms, user_forms)

        # Pass context to template and render page.
        context = {
            "zipped_data": zipped_data,
            "user_metadata": all_user_metadata,
            "metadata_forms": metadata_forms
        }
        return render(request, "manageaccount.html", context)
    else:
        return redirect(login_user)
