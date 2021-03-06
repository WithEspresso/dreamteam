from django.contrib.auth.models import User
from django import forms
from .models import PaidTimeOffEntry, Expenses, UserMetaData
from .validators import validate_image_file
from .validators import validate_year_entry


class LoginForm(forms.Form):
    """
    Form used to login to the payroll site.
    Passwords are represented as stars.
    """
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    # Meta Information about your class.
    class Meta:
        fields = ['username', 'password']


class TimeSheetForm(forms.Form):
    """
    Form used to entry time sheets.
    """
    number_hours = forms.IntegerField(widget=forms.NumberInput(
        attrs={'class': 'form-control',
               'min': '0',
               'max': '24',
               'value': '8.00',
               'name': "hours",
               'aria-label': "...",
               'type': "number"
               }
    ))
    number_hours.widget.attrs["onchange"] = "calculateTotal()"


class UserSignUpForm(forms.ModelForm):
    """
    Form used to register users.
    """
    # Changes it from plain text to hashing
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'containder-inside-form',
              }))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'containder-inside-form',
              }))
    email = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'containder-inside-form',
              }))
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'containder-inside-form',
              }))
    last_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'containder-inside-form',
              }))

    # Meta Information about your class.
    class Meta:
        model = User
        # What fields do we want to appear on the form?
        fields = ['username', 'password', 'email', 'first_name', 'last_name']


class UserForm(forms.ModelForm):
    """
    Form used for updating user information.
    """
    # Changes it from plain text to hashing
    email = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'containder-inside-form',
              }))
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'containder-inside-form',
              }))
    last_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'containder-inside-form',
              }))

    # Meta Information about your class.
    class Meta:
        model = User
        # What fields do we want to appear on the form?
        fields = ['email', 'first_name', 'last_name']


class UserMetaDataForm(forms.ModelForm):
    """
    Form used for updating user meta data.
    """
    GROUP_CHOICES = [
        ('Employee', 'Employee'),
        ('Manager', 'Manager'),
        ('Human Resources', 'HumanResources')
    ]

    address = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Enter address.',
               'class': 'containder-inside-form',
               }))
    social_security_number = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Enter social security number.',
               'class': 'containder-inside-form',
               }))
    company = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'containder-inside-form',
              }))
    group = forms.ChoiceField(choices=GROUP_CHOICES, widget=forms.RadioSelect())

    # Meta Information about your class.
    class Meta:
        model = UserMetaData
        # What fields do we want to appear on the form?
        fields = ['address', 'social_security_number', 'company', 'group']


class PaidTimeOffRequestForm(forms.ModelForm):
    """
    Form used for submitting PTO requests
    """
    # User is automatically retrieved from the request.user method in the view.
    # Status is only visible to the manager
    class Meta:
        model = PaidTimeOffEntry
        fields = ['date', 'hours', 'status']


class ExpenseRequestForm(forms.ModelForm):
    """
    Form used for submitting expense requests.
    """
    title = forms.CharField(widget=forms.TextInput(
    {
        'placeholder': "Enter title",
        'width':"48",
    }))
    amount = forms.DecimalField(widget=forms.NumberInput(
        {
            'min': "0",
            'width': "48",
        }
    ))
    date = forms.DateField(widget=forms.DateInput())
    file = forms.FileField(label="Upload receipt",
                           help_text="Maximum file size is 2 megabytes",
                           validators=[validate_image_file])

    # User is automatically retrieved from the request.user method in the view.
    # Status is only visible to the manager
    class Meta:
        model = Expenses
        fields = ['title', 'amount', 'file']
