from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    name = models.CharField(max_length=100, null=False)
    category = models.CharField(max_length=20, null=False)
    info = models.CharField(max_length=100, null=False)
    description = models.CharField(max_length=100)
    start_data = models.DateField(null=False)
    end_data = models.DateField()
    done = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
