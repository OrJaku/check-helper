from django.contrib import admin
from django.urls import path

from tasks.views import home, tasks_list, user_login, user_logout, change_task_status

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', home, name='home'),
    path('tasks_list/', tasks_list, name='tasks_list'),
    path('user_login/', user_login, name='user_login'),
    path('user_logout/', user_logout, name='user_logout'),
    path('change_task_status/', change_task_status, name='change_task_status'),

]