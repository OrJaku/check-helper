from django.contrib import admin
from django.urls import path

from tasks.views import home, tasks_list, user_login, user_logout

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', home, name='home'),
    path('tasks_list/', tasks_list, name='tasks_list'),
    path('user_login/', user_login, name='user_login'),
    path('user_logout/', user_logout, name='user_logout'),

]
