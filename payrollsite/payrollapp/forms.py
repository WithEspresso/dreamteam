from django.contrib.auth.models import User
from django import forms
from .models import PaidTimeOffRequests


class LoginForm(forms.ModelForm):
    # Changes it from plain text to hashing
    password = forms.CharField(widget=forms.PasswordInput)

    # Meta Information about your class.
    class Meta:
        model = User
        # What fields do we want to appear on the form?
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