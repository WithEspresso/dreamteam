# Generated by Django 2.0.3 on 2018-04-24 17:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('payrollapp', '0006_auto_20180418_0016'),
    ]

    operations = [
        migrations.CreateModel(
            name='HumanResourcesData',
            fields=[
                ('human_resources_data_id', models.AutoField(primary_key=True, serialize=False)),
                ('is_activated', models.BooleanField(default=True)),
                ('is_human_resources', models.BooleanField(default=False)),
                ('is_manager', models.BooleanField(default=False)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='paidtimeoffrequests',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Denied', 'Denied')], default='Pending', max_length=10),
            preserve_default=False,
        ),
    ]
