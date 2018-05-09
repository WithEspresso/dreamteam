from django.contrib.auth.models import User
from django import forms
from .models import PaidTimeOffEntry, Expenses, UserMetaData
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


class UserMetaDataForm(forms.ModelForm):

    # Meta Information about your class.
    class Meta:
        model = UserMetaData
        # What fields do we want to appear on the form?
        fields = ['address', 'social_security_number', 'group', 'company']


class PaidTimeOffSubmissionForm(forms.ModelForm):


    class Meta:
        pass


class PaidTimeOffRequestForm(forms.ModelForm):
    # User is automatically retrieved from the request.user method in the view.
    # Status is only visible to the manager
    class Meta:
        model = PaidTimeOffEntry
        fields = ['date', 'hours', 'status']


class ExpenseRequestForm(forms.ModelForm):
    file = forms.FileField(label="Select an image to upload.",
                           help_text="Maximum file size is 2 megabytes",
                           validators=[validate_image_file])

    # User is automatically retrieved from the request.user method in the view.
    # Status is only visible to the manager
    class Meta:
        model = Expenses
        fields = ['title', 'amount', 'file']


class ApprovalForm(forms.Form):
    """
    Form to search the website.
    User selects a search algorithm with the drop down menu and enters a query.
    Query is stored as the value in this form.
    """
    select_choices = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Denied', 'Denied'),
    )
    # time_sheet_id = forms.CharField(widget=forms.HiddenInput(), initial="Pending")
    status = forms.ChoiceField(widget=forms.Select, choices=select_choices)
