from django.db import models
from django.db.models import Sum

from django.contrib.auth.models import User
from django.utils.timezone import now

from django.conf.urls import *

import calendar
import datetime

# Statuses for approvals.
STATUS_CHOICE = (
    ('Pending', 'Pending'),
    ('Approved', 'Approved'),
    ('Denied', 'Denied'))

# Statuses for users.
USER_STATUS = (
    ('Active', 'Active'),
    ('Terminated', 'Terminated'),
    ('No current affiliation', 'No current affiliation')
)

# User groups to classify users. Corresponds with Django's
# build in user groups authentication system.
USER_GROUPS = (
    ('Employee', 'Employee'),
    ('Manager', 'Manager'),
    ('Human Resources', 'Human Resources')
)

# Number of work hours every four weeks.
FOUR_WEEKS = 160


class UserMetaData(models.Model):
    """
    A data structure for the database table to represent
    user meta data. User meta data includes data about their
    address, ssn, what company their work for,
    and what role their have in the company.
    """
    user_meta_data_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="django_user_id")
    address = models.CharField(max_length=255)
    social_security_number = models.IntegerField()
    group = models.CharField(max_length=32, choices=USER_GROUPS, default='Employee')
    user_status = models.CharField(max_length=25, choices=USER_STATUS, default='Active')
    company = models.CharField(max_length=255, unique=False, default="No company")

    def __str__(self):
        """
        The string representation of the user meta data
        @rtype: String
        @return: The string representation of the user meta data
        """
        return str(self.user_id) + "'s meta data"


class TimeSheetApprovals(models.Model):
    """
    A data structure for the database table to represent
    time sheet approvals. This table is used as a foreign key
    to relate all time sheet entries to a single approval.
    """
    time_sheet_approvals_id = models.AutoField(primary_key=True)
    date_submitted = models.DateField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICE, default="Pending")
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    @staticmethod
    def get_all_by_username(username):
        """
        Returns all time sheet approvals for the given user id.
        @type  username: User object
        @param username: A user to search for
        @rtype: queryset
        @return: Matching time sheet approvals for the given username
        """
        results = TimeSheetApprovals.objects.filter(user_id__username=username)
        return results

    def get_all_entries_by_submission(self):
        """
        Returns all entries related to the submission
        @rtype: queryset
        @return: All entries related to the time sheet submission
        """
        id = self.time_sheet_approvals_id
        results = TimeSheetEntry.objects.filter(time_sheet_approvals_id=id)
        return results

    def get_total_hours(self):
        """
        Calculates the total hours for the time sheet submission.
        @rtype: integer
        @return: The total hours for the time sheet submission.
        """
        all_entries = self.get_all_entries_by_submission()
        total_hours = all_entries.aggregate(Sum('number_hours')).get('number_hours__sum')
        return total_hours


class TimeSheetEntry(models.Model):
    """
    A data structure for the database table to represent
    time sheet entries. Each entry is related to a
    time sheet approval.
    """
    time_sheet_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    number_hours = models.IntegerField()
    time_sheet_approvals_id = models.ForeignKey(TimeSheetApprovals, on_delete=models.CASCADE)

    @staticmethod
    def get_all_submissions_by_month(username, date=datetime.datetime.now()):
        """
        Gets all submissions of time sheets for that month. Default
        month is the current month.
        @type  username: A User object
        @param username: User to search for.
        @type  date:    datetime.datetime
        @param date:    Month to search for
        @rtype: queryset
        @return: All submissions for the given user in the month provided
        """
        month = date.month
        year = date.year
        start_day = calendar.monthrange(year, month)[0]
        end_day = calendar.monthrange(year, month)[1]
        start_date = datetime.date(year, month, start_day)
        end_date = datetime.date(year, month, end_day)
        results = TimeSheetEntry.objects.filter(user_id__username__exact=username).filter(
            date__range=[start_date, end_date])
        return results

    @staticmethod
    def calculate_pay_period_total_hours(username, date=datetime.datetime.now()):
        """
        Calculates the total hours for the current pay period. The default
        pay period is the current month as a datetime. Calculates the first and last
        day of the month and uses that to search the database for time sheet submissions
        within the pay period.
        @type  username: A User object
        @param username: The User to search for
        @type  date: datetime.datetime
        @param date: datetime.datetime
        @rtype: integer
        @return: Total hours in the pay period
        """
        start_date = datetime.date(date.year, date.month, 1)
        end_date = datetime.date(date.year, date.month, calendar.mdays[date.month])
        total_hours = TimeSheetEntry.objects.filter(date__range=[start_date, end_date]) \
            .filter(user_id__username__exact=username) \
            .aggregate(Sum('number_hours')).get('number_hours__sum')
        return total_hours

    @staticmethod
    def get_time_sheet_by_company(username):
        """
        @type  username: User object
        @param username: A User to search for
        @rtype:     queryset
        @return:    queryset of matching timesheet entries.
        """
        matching_timesheets = TimeSheetEntry.objects.filter.all()
        return matching_timesheets

    def __str__(self):
        """
        Returns a string representation of the Time Sheet object.
        @rtype:     String
        @return:    String representation of time sheet
        """
        return str(self.user_id) + "'s time sheet, " + str(self.time_sheet_id)


class PaycheckInformation(models.Model):
    """
    A data structure for the database table to represent
    paycheck information. Paychecks are calculated
    based on approved time sheet submissions.
    """
    paycheck_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    payday = models.DateField(default=now)
    amount = models.DecimalField(decimal_places=2, max_digits=16)
    witholdings = models.DecimalField(decimal_places=2, max_digits=16)

    @staticmethod
    def search_by_time_period(start_date, end_date, username):
        """
        Searches the database for entries within the given
        time period for the user.
        @type  start_date: datetime.datetime
        @param start_date: The lower end of the range to search for
        @type    end_date: datetime.datetime
        @param   end_date: The upper bound of the range to search for
        @type    username: A User object
        @param   username: The username to match results
        @rtype:     queryset
        @return:    A queryset of matching database entries.
        """
        results = PaycheckInformation.objects.filter(user_id__username__exact=username).filter(
            payday__range=[start_date, end_date])
        return results

    @staticmethod
    def get_last_years_history():
        """
        Gets the last twelve calendar months.
        @rtype:  list
        @return: A list of the last twelve months.
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
    """
    Creates a path for file uploads.
    File will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    @type  instance:    an instance of the Expenses mdoel
    @param instance:    The instance of the model object.
    @type  filename:    String
    @param filename:    The name of the file.
    @rtype:  String
    @return: the path where the file will be saved
    """
    return 'expenses/user_{0}/{1}'.format(instance.user_id.id, filename)


class Expenses(models.Model):
    """
    A data structure for the database table to represent
    expense reimbursement requests.
    """
    expense_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(decimal_places=2, max_digits=16)
    file = models.ImageField(upload_to=expense_directory_path, null=True)
    description = models.CharField(max_length=255, default="No description.")
    date = models.DateField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICE)

    def get_users_fullname(self):
        """
        Returns the user's full name.
        @rtype: String
        @return: The user's full name
        """
        return str(self.user_id.first_name) + " " + str(self.user_id.last_name)

    def get_user_id(self):
        """
        A string representation of the user's id, the primary key.
        @rtype: String
        @return: A string representation of the primary key
        """
        return str(self.user_id.id)


class PaidTimeOffApproval(models.Model):
    """
    A data structure for the database table to represent
    paid time off approvals. Each paid time off entry
    is related to an approval.
    """
    paid_time_off_approval_id = models.AutoField(primary_key=True)
    date_submitted = models.DateField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICE, default="Pending")
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    @staticmethod
    def get_all_by_username(username):
        """
        Searches the database for all requests matching the given username.
        @param username: A username denoting a User object
        @rtype: queryset
        @return: All Paid time off approval objects that match the given User
        """
        results = PaidTimeOffApproval.objects.filter(user_id__username=username)
        return results

    @staticmethod
    def get_total_approved_pto(username):
        """
        Calculates how many hours of approved pto a user has.
        @param username: A username used to denote a User object
        @rtype: integer
        @return: The total approved hours
        """
        results = PaidTimeOffApproval.objects.filter(user_id__username=username).filter(status="Approved")
        total_approved_hours = 0
        for entry in results:
            total_approved_hours += int(entry.get_total_hours())
        return total_approved_hours

    def get_all_entries_by_submission(self):
        """
        Returns all time sheet entries for the approval ID
        @rtype: queryset
        @return: A queryset of all paid time off entries.
        """
        id = self.paid_time_off_approval_id
        results = PaidTimeOffEntry.objects.filter(paid_time_off_approval_id=id)
        return results

    def get_total_hours(self):
        """
        Calculates the total hours of all entries submitted for this approval.
        @rtype: dict
        @return: The total hours for the submission's entries.
        """
        entries = self.get_all_entries_by_submission()
        total_hours = entries.aggregate(Sum('hours')).get('hours__sum')
        return total_hours


class PaidTimeOffEntry(models.Model):
    """
    A data structure for the database table to represent
    paid time off entries. Each entry is related to an
    approval row in the Paid Time Off Approvals table.
    """
    paid_time_off_request_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    hours = models.IntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICE, default="Pending")
    paid_time_off_approval_id = models.ForeignKey(PaidTimeOffApproval, on_delete=models.CASCADE)

    def __str__(self):
        """
        Returns a string representation of the paid time off entry.
        @rtype:     String
        @return:    a string representation of the pto entry
        """
        return str(self.user_id) + "'s pto request for " + str(self.date) + " in approval: "


class PaidTimeOffHours(models.Model):
    """
    A data structure for the database table to represent
    remaining pto hours for a user.
    """
    vacation_hours_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    remaining_hours = models.IntegerField(default=FOUR_WEEKS)

    def __str__(self):
        """
        A string representation
        @rtype: String
        @return: A string representation of remaining pto hours
        """
        return "PTO Hours for: " + str(self.user_id) + str(self.remaining_hours)
