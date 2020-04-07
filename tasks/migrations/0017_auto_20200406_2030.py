# Generated by Django 3.0.4 on 2020-04-06 20:30

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0016_dailytask_completed'),
    ]

    operations = [
        migrations.AddField(
            model_name='dailytask',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='dailytask',
            name='first_date',
            field=models.DateField(default=datetime.datetime(2020, 4, 6, 20, 30, 27, 575634)),
        ),
    ]