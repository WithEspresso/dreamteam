"""
This file contains methods for validating form input.
"""
from django import forms


def validate_year_entry(value):
    import datetime
    now = datetime.datetime.now()
    current_year = int(now.year)
    if value < 1990 or value > current_year:
        raise forms.ValidationError('The year entered is invalid.')


def validate_image_file(value):
    import os
    extension = os.path.splitext(value.name)[1]
    valid_extensions = ['.jpg', '.png', '.jpeg']
    if extension not in valid_extensions:
        raise forms.ValidationError('An image file is required. (.jpg and .png file extensions only)')