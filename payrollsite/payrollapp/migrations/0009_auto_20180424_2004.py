# Generated by Django 2.0.3 on 2018-04-25 03:04

from django.conf import settings
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('payrollapp', '0008_auto_20180424_1550'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='TimeSheet',
            new_name='TimeSheetSubmission',
        ),
        migrations.AlterField(
            model_name='paycheckinformation',
            name='payday',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
