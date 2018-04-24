from django.contrib.auth.models import User
from django import forms
from .models import PaidTimeOffRequests, Expenses
from .validators import validate_image_file
from .validators import validate_year_entry


class LoginForm(forms.Form):
    # Changes it from plain text to hashing
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    # Meta Information about your class.
    class Meta:
        fields = ['username', 'password']


class UserForm(forms.ModelForm):
    # Changes it from plain text to hashing
    password = forms.CharField(widget=forms.PasswordInput)

    # Meta Information about your class.
    class Meta:
        model = User
        # What fields do we want to appear on the form?
        fields = ['username', 'email', 'first_name', 'last_name', 'password']


class PaidTimeOffForm(forms.ModelForm):
    # User is automatically retrieved from the request.user method in the view.
    # Status is only visible to the manager
    class Meta:
        model = PaidTimeOffRequests
        fields = ['date', 'hours']


MONTH_CHOICES = (
    ('jan', 'January'),
    ('feb', 'February'),
    ('mar', 'March'),
    ('apr', 'April'),
    ('may', 'May'),
    ('jun', 'June'),
    ('jul', 'July'),
    ('aug', 'August'),
    ('sep', 'September'),
    ('oct', 'October'),
    ('nov', 'November'),
    ('dec', 'December'),
)


class PaycheckSearchForm(forms.Form):
    # Form to search and retrieve paychecks from a pay period.
    month = forms.ChoiceField(widget=forms.Select, choices=MONTH_CHOICES)
    year = forms.IntegerField(validators=[validate_year_entry])

    class Meta:
        fields = ['month', 'year']


class ExpenseRequestForm(forms.ModelForm):
    file = forms.FileField(label="Select an image to upload.",
                           help_text="Maximum file size is 2 megabytes",
                           validators=[validate_image_file])

    # User is automatically retrieved from the request.user method in the view.
    # Status is only visible to the manager
    class Meta:
        model = Expenses
        fields = ['title', 'amount', 'file']
