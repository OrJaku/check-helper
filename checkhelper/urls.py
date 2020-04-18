from django.contrib import admin
from django.urls import path

from tasks.views import home, \
    tasks_list, \
    user_login, \
    user_logout, \
    change_task_status, \
    task_detail, \
    update_task, \
    delete_task, \
    daily_tasks_settings, \
    delete_daily_task, \
    searching_tasks

from notes.views import notes_list, \
    delete_note, \
    searching_notes, \
    update_note


urlpatterns = [
    path('admin/', admin.site.urls),

    path('', home, name='home'),

    path('tasks_list/', tasks_list, name='tasks_list'),
    path('tasks_list/<int:task_id>', task_detail, name='task_detail'),
    path('tasks_list/<int:task_id>/update_task', update_task, name='update_task'),
    path('change_task_status/', change_task_status, name='change_task_status'),
    path('delete_task/', delete_task, name='delete_task'),
    path('daily_tasks_settings/', daily_tasks_settings, name='daily_tasks_settings'),
    path('delete_daily_task/', delete_daily_task, name='delete_daily_task'),
    path('searching_tasks/', searching_tasks, name='searching_tasks'),

    path('user_login/', user_login, name='user_login'),
    path('user_logout/', user_logout, name='user_logout'),

    path('notes_list/', notes_list, name='notes_list'),
    path('delete_note/', delete_note, name='delete_note'),
    path('update_note/', update_note, name='update_note'),
    path('searching_notes/', searching_notes, name='searching_notes'),
]


