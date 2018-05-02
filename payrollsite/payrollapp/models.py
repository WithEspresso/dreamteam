from django.db import models
from django.db.models import Sum

from django.contrib.auth.models import User
from django.utils.timezone import now

import calendar
from datetime import datetime

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


class HumanResourcesData(models.Model):
    human_resources_data_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    is_activated = models.BooleanField(default=True)
    is_human_resources = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)


class TimeSheetSubmission(models.Model):
    time_sheet_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    number_hours = models.IntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICE)

    @staticmethod
    def calculate_pay_period_total_hours(username, date=now()):
        """
        Calculates the total hours for the current pay period. The default
        pay period is the current month as a datetime. Calculates the first and last
        day of the month and uses that to search the database for time sheet submissions
        within the pay period.
        :param username:
        :param date:
        :return:The total hours for the pay period of the user.
        """
        start_date = datetime(date.year, date.month, 1)
        end_date = datetime(date.year, date.month, calendar.mdays[date.month])
        total_hours = TimeSheetSubmission.objects.filter(date__range=[start_date, end_date])\
            .filter(user_id__username__exact=username)\
            .aggregate(Sum('number_hours'))
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
        matching_timesheets = TimeSheetSubmission.objects.filter.all()
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
    status = models.CharField(max_length=10, choices=STATUS_CHOICE)


class ExpenseRequest(models.Model):
    expense_request_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    approved = models.BooleanField(default=False)


class PaidTimeOff(models.Model):
    paid_time_off_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)


class PaidTimeOffRequests(models.Model):
    paid_time_off_request_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    hours = models.IntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICE, default="Pending")

    def __str__(self):
        return str(self.user_id) + "'s pto request for " + str(self.date)


class Approvals(models.Model):
    approval_id = models.AutoField(primary_key=True)
    status = models.CharField(max_length=20)


class PaidTimeOffHours(models.Model):
    vacation_hours_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    remaining_hours = models.IntegerField(default=FOUR_WEEKS)
