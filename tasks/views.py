from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
import time
from .models import Task


def home(request, *args, **kwargs):
    print(args, kwargs)
    print(request.user)
    return render(request, 'home.html', {})


@login_required(login_url='/user_login/')
def tasks_list(request):
    if request.method == "POST":
        name = request.POST.get("name")
        print("NAME", name)
        category = request.POST.get("category")
        info = request.POST.get("info")
        description = request.POST.get("description")
        start_data = request.POST.get("start_data")
        end_data = request.POST.get("end_data")
        new_task = Task.objects.create(
                                    name=name,
                                    category=category,
                                    info=info,
                                    description=description,
                                    start_data=start_data,
                                    end_data=end_data,
                                    user=request.user
                                    )
        new_task.save()
        return redirect('/tasks_list/')

    tasks_user = Task.objects.all().filter(user=request.user).order_by("end_data")

    context = {
        'objects': tasks_user,
    }
    return render(request, 'tasks_list.html', context)


@login_required(login_url='/user_login/')
def task_detail(request, task_id):
    task = Task.objects.get(id=task_id)
    time_data = time.strftime("%Y%m%d-%H%M%S")
    context = {
        'task': task,
    }
    return render(request, 'task_detail.html', context)


def change_task_status(request):
    if request.method == "POST":
        task_id = request.POST["change_status"]
        task = Task.objects.get(id=task_id)
        if task.done:
            task.done = False
        else:
            task.done = True
        task.save()
        return redirect(f"/tasks_list/{task_id}")
    return render(request, 'tasks_list.html', {})


def update_task(request, task_id):
    if request.method == "POST":
        task = Task.objects.get(id=task_id)
        task.name = request.POST["name"]
        print(task.name)
        return redirect(f'/tasks_list/{task_id}')
    return render(request, 'tasks_list.html', {})


def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/tasks_list/')

        else:
            print("invalid login or password")
        return render(request, 'home.html', {})

    else:
        return render(request, 'user_login.html', {})


def user_logout(request):
    logout(request)
    return redirect('/')




