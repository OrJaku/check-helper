from django.db import models
from django.contrib.auth.models import User


class Brand(models.Model):
    name = models.CharField(max_length=30, null=False)

    def __str__(self):
        return '%s' % self.name


class Task(models.Model):
    name = models.CharField(max_length=100, null=False)
    category = models.CharField(max_length=20, null=False)
    info = models.CharField(max_length=100, null=False)
    description = models.CharField(max_length=100)
    start_data = models.DateField(null=False)
    end_data = models.DateField()
    done = models.BooleanField(default=False)
    priority = models.IntegerField(default=1)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='brand')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')

    def __str__(self):
        return 'Task: %s' % self.name


class DailyTask(models.Model):
    name = models.CharField(max_length=100, null=False)
    category = models.CharField(max_length=20, null=False)
    description = models.CharField(max_length=100)
    tag = models.CharField(max_length=20, null=False)
    # user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_daily')

    def __str__(self):
        return 'Tag: %s' % self.tag

