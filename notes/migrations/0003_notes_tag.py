# Generated by Django 3.0.4 on 2020-04-25 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0002_notes_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='notes',
            name='tag',
            field=models.CharField(default='NoTag', max_length=20),
        ),
    ]
