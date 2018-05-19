"""
This file contains methods for validating form input.
"""
from django import forms


def validate_year_entry(value):
    """
    Validates that a year provided is greater than 1990 or
    equal to or less than the current year.
    @type  value: String
    @param value:
    @return: None
    @raise: ValidationError
    """
    import datetime
    now = datetime.datetime.now()
    current_year = int(now.year)
    if value < 1990 or value > current_year:
        raise forms.ValidationError('The year entered is invalid.')


def validate_image_file(value):
    """
    Validates that the image file provided is actually an image
    file. (.jpeg, .jpg, or .png). Throws a validation
    error if another extension is provided.
    @type  value: String
    @param value: The name of the image file to be uploaded
    @return: None
    @raise: ValidationError
    """
    import os
    extension = os.path.splitext(value.name)[1]
    valid_extensions = ['.jpg', '.png', '.jpeg']
    if extension not in valid_extensions:
        raise forms.ValidationError('An image file is required. (.jpg and .png file extensions only)')