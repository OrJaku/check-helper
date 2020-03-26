from django.db import models


class Task(models.Model):
    name = models.CharField(max_length=100, null=False)
    category = models.CharField(max_length=20, null=False)
    info = models.CharField(max_length=100, null=False)
    description = models.CharField(max_length=100)
    start_data = models.DateField(null=False)
    end_data = models.DateField()
    done = models.BooleanField(default=False)
