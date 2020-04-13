from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


class Notes(models.Model):
    name = models.CharField(max_length=100, null=False)
    description = models.CharField(max_length=1000)
    date = models.DateField(default=now)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_note')

    def __str__(self):
        return 'Note: %s - %s' % (self.name, self.date)
