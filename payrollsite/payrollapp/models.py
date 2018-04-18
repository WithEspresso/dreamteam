from django.db import models
from django.contrib.auth.models import User


STATUS_CHOICE = (
    ('Pending', 'Pending'),
    ('Approved', 'Approved'),
    ('Denied', 'Denied'))


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
    user_status = models.CharField(max_length=25)


class TimeSheet(models.Model):
    time_sheet_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    number_hours = models.IntegerField()

    def __str__(self):
        return self.user_id + "'s time sheet, " + self.time_sheet_id


class Wages(models.Model):
    wages_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=20)
    tax_withholding = models.DecimalField(decimal_places=2, max_digits=16)

    def __str__(self):
        return self.user_id + "'s " + "wages"


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

    def __str__(self):
        return str(self.user_id) + "'s pto request for " + str(self.date)


class Approvals(models.Model):
    approval_id = models.AutoField(primary_key=True)
    status = models.CharField(max_length=20)
