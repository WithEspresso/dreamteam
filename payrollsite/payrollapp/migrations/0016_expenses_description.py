# Generated by Django 2.0.3 on 2018-05-08 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payrollapp', '0015_auto_20180502_0133'),
    ]

    operations = [
        migrations.AddField(
            model_name='expenses',
            name='description',
            field=models.CharField(default='No description.', max_length=255),
        ),
    ]
