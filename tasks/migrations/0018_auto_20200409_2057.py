# Generated by Django 3.0.4 on 2020-04-09 20:57

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0017_auto_20200406_2030'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dailytask',
            name='first_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
