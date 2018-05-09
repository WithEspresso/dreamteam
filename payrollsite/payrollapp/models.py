from django.db import models
from django.db.models import Sum

from django.contrib.auth.models import User
from django.utils.timezone import now

from django.conf.urls import *

import calendar
import datetime

STATUS_CHOICE = (
    ('Pending', 'Pending'),
    ('Approved', 'Approved'),
    ('Denied', 'Denied'))

USER_STATUS = (
    ('Active', 'Active'),
    ('Terminated', 'Terminated'),
    ('No current affiliation', 'No current affiliation')
)

USER_GROUPS = (
    ('Employee', 'Employee'),
    ('Manager', 'Manager'),
    ('Human Resources', 'Human Resources')
)

# Number of work hours every four weeks.
FOUR_WEEKS = 160


class Manager(models.Model):
    manager_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)


class HumanResources(models.Model):
    human_resources_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)


class Employee(models.Model):
    employee_id = models.AutoField(primary_key=True)
    manager_id = models.ForeignKey(Manager, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)


class UserMetaData(models.Model):
    user_meta_data_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    social_security_number = models.IntegerField()
    group = models.CharField(max_length=32, choices=USER_GROUPS, default='Employee')
    user_status = models.CharField(max_length=25, choices=USER_STATUS, default='Active')
    company = models.CharField(max_length=255, unique=False, default="No company")

    def __str__(self):
        return str(self.user_id) + "'s meta data"


class HumanResourcesData(models.Model):
    human_resources_data_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    is_activated = models.BooleanField(default=True)
    is_human_resources = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)


class TimeSheetApprovals(models.Model):
    time_sheet_approvals_id = models.AutoField(primary_key=True)
    date_submitted = models.DateField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    @staticmethod
    def get_all_by_username(username):
        results = TimeSheetApprovals.objects.filter(user_id__username=username)
        return results

    def get_all_entries_by_submission(self):
        """
        Returns all time sheet entries for the approval ID
        :param username to search for
        :param date: optional pay period to search for
        :return: A queryset of all submissions
        """
        id = self.time_sheet_approvals_id
        results = TimeSheetEntry.objects.filter(time_sheet_approvals_id=id)
        return results

    def get_total_hours(self):
        """
        Calculates the total hours in each submission.
        :return: The total hours worked as an integer.
        """
        all_entries = self.get_all_entries_by_submission()
        total_hours = all_entries.aggregate(Sum('number_hours')).get('number_hours__sum')
        return total_hours


class TimeSheetEntry(models.Model):
    time_sheet_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    number_hours = models.IntegerField()
    time_sheet_approvals_id = models.ForeignKey(TimeSheetApprovals, on_delete=models.CASCADE)

    @staticmethod
    def get_all_submissions_by_month(username, date=datetime.datetime.now()):
        """
        Default is getting the current datetime and getting all submissions
        within the month.
        :param username to search for
        :param date: optional pay period to search for
        :return: A queryset of all submissions
        """
        month = date.month
        year = date.year
        start_day = calendar.monthrange(year, month)[0]
        end_day = calendar.monthrange(year, month)[1]
        start_date = datetime.date(year, month, start_day)
        end_date = datetime.date(year, month, end_day)
        results = TimeSheetEntry.objects.filter(user_id__username__exact=username).filter(date__range=[start_date, end_date])
        return results

    @staticmethod
    def calculate_pay_period_total_hours(username, date=datetime.datetime.now()):
        """
        Calculates the total hours for the current pay period. The default
        pay period is the current month as a datetime. Calculates the first and last
        day of the month and uses that to search the database for time sheet submissions
        within the pay period.
        :param username:
        :param date:
        :return:The total hours for the pay period of the user.
        """
        start_date = datetime.date(date.year, date.month, 1)
        end_date = datetime.date(date.year, date.month, calendar.mdays[date.month])
        total_hours = TimeSheetEntry.objects.filter(date__range=[start_date, end_date])\
            .filter(user_id__username__exact=username)\
            .aggregate(Sum('number_hours')).get('number_hours__sum')
        return total_hours

    @staticmethod
    def get_time_sheet_by_company(username):
        """
        Searches the database for time sheets by user.
        :param username:
        :return:
        """
        # matching_timesheets = TimeSheetSubmission.objects.filter(user_id__username__exact=username)
        # <queryset>.filter(<ForeignKeyTable>__<ForeignKeyColumn>__exact=<company_name>)
        # matching_timesheets = matching_timesheets.filter(user)
        matching_timesheets = TimeSheetEntry.objects.filter.all()
        return matching_timesheets

    def __str__(self):
        return str(self.user_id) + "'s time sheet, " + str(self.time_sheet_id)


class PaycheckInformation(models.Model):
    paycheck_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    payday = models.DateField(default=now)
    amount = models.DecimalField(decimal_places=2, max_digits=16)
    witholdings = models.DecimalField(decimal_places=2, max_digits=16)

    @staticmethod
    def search_by_time_period(start_date, end_date, username):
        results = PaycheckInformation.objects.filter(user_id__username__exact=username).filter(payday__range=[start_date, end_date])
        return results

    @staticmethod
    def get_last_years_history():
        """
        Returns a dictionary of the last twelve months' paychecks.
        :return:
        """
        right_now = datetime.datetime.now()
        current_month = right_now.month
        last_twelve_months = []
        for i in range(0, 12):
            next_month = current_month - i
            if next_month <= 0:
                next_month += 12
            last_twelve_months.append(calendar.month_name[next_month])
        last_twelve_months.reverse()
        return last_twelve_months

    def __str__(self):
        return str(self.user_id) + "'s " + "wages"


def expense_directory_path(instance, filename):
        # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
        return 'expenses/user_{0}/{1}'.format(instance.user_id.id, filename)


class Expenses(models.Model):
    expense_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(decimal_places=2, max_digits=16)
    file = models.ImageField(upload_to=expense_directory_path, null=True)
    description = models.CharField(max_length=255, default="No description.")
    date = models.DateField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICE)

    def get_users_fullname(self):
        return str(self.user_id.first_name) + " " + str(self.user_id.last_name)

    def get_user_id(self):
        return str(self.user_id.id)


class ExpenseRequest(models.Model):
    expense_request_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    approved = models.BooleanField(default=False)


class PaidTimeOffApproval(models.Model):
    paid_time_off_approval_id = models.AutoField(primary_key=True)
    date_submitted = models.DateField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICE, default="Pending")
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    @staticmethod
    def get_all_by_username(username):
        results = PaidTimeOffApproval.objects.filter(user_id__username=username)
        return results

    def get_all_entries_by_submission(self):
        """
        Returns all time sheet entries for the approval ID
        :param username to search for
        :param date: optional pay period to search for
        :return: A queryset of all submissions
        """
        id = self.paid_time_off_approval_id
        results = PaidTimeOffEntry.objects.filter(paid_time_off_approval_id=id)
        return results

    def get_total_hours(self):
        entries = self.get_all_entries_by_submission()
        total_hours = entries.aggregate(Sum('hours')).get('hours__sum')
        return total_hours


class PaidTimeOffEntry(models.Model):
    paid_time_off_request_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    hours = models.IntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICE, default="Pending")
    paid_time_off_approval_id = models.ForeignKey(PaidTimeOffApproval, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user_id) + "'s pto request for " + str(self.date) + " in approval: "


class Approvals(models.Model):
    approval_id = models.AutoField(primary_key=True)
    status = models.CharField(max_length=20)


class PaidTimeOffHours(models.Model):
    vacation_hours_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    remaining_hours = models.IntegerField(default=FOUR_WEEKS)
