# Generated by Django 2.0.3 on 2018-04-18 06:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payrollapp', '0003_auto_20180417_2221'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paidtimeoffrequests',
            name='status',
        ),
        migrations.AddField(
            model_name='expenses',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Denied', 'Denied')], default='Pending', max_length=10),
            preserve_default=False,
        ),
    ]
