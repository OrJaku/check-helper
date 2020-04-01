from django.contrib import admin
from .models import Task, Brand, DailyTask

admin.site.register(Task)
admin.site.register(Brand)
admin.site.register(DailyTask)

