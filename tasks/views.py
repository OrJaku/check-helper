from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import Task
import datetime
from datetime import timedelta


def home(request, *args, **kwargs):
    print(request.user)
    return render(request, 'home.html', {})


@login_required(login_url='/user_login/')
def tasks_list(request):
    sort = "end_data"
    current_date = datetime.date.today()

    if request.method == "POST":
        if "sort" in request.POST:
            sort = request.POST.get("sort")
            print("SORT", sort)
            print(request.POST)
            if sort[0] == "-":
                print(sort[0])
                pass
            else:
                sort = "" + sort
        else:
            name = request.POST.get("name")

            category = request.POST.get("category")
            category = category.title()

            info = request.POST.get("info")
            if name == "":
                name = 'Empty'
            else:
                pass

            description = request.POST.get("description")

            priority = request.POST.get("priority")

            start_data = request.POST.get("start_data")
            if start_data == "":
                start_data = current_date
            else:
                pass
            try:
                delta = int(request.POST.get("delta"))
            except ValueError:
                delta = ""

            if delta == "":
                delta = 10
            else:
                pass

            end_data = request.POST.get("end_data")
            if end_data == "":
                end_data = current_date + timedelta(delta)
            else:
                pass

            new_task = Task.objects.create(
                                        name=name,
                                        category=category,
                                        info=info,
                                        description=description,
                                        start_data=start_data,
                                        end_data=end_data,
                                        priority=priority,
                                        user=request.user,
                                        )
            new_task.save()
            return redirect('/tasks_list/')

    tasks_user = Task.objects.all().filter(user=request.user).order_by(sort)
    tasks_user_archive = Task.objects.all().filter(user=request.user).order_by(sort)
    date_difference = []

    def zipping(lists):
        for task in lists:
            difference = task.end_data - current_date
            days = str(difference).split(" ")
            try:
                days = int(days[0])
            except ValueError:
                days = 0
            date_difference.append(days)
        zipped_list = zip(tasks_user, date_difference)
        return zipped_list

    tasks_user_with_date_difference = zipping(tasks_user)
    tasks_user_archive_with_date_difference = zipping(tasks_user_archive)

    context = {
        'tasks': tasks_user_with_date_difference,
        'tasks_archive': tasks_user_archive_with_date_difference,

    }
    return render(request, 'tasks_list.html', context)


@login_required(login_url='/user_login/')
def task_detail(request, task_id):
    task = Task.objects.get(id=task_id)
    context = {
        'task': task,
    }
    return render(request, 'task_detail.html', context)


@login_required(login_url='/user_login/')
def change_task_status(request):
    if request.method == "POST":
        list_ = False
        if "change_status" in request.POST:
            task_id = request.POST.get("change_status")

        elif "change_status_list" in request.POST:
            task_id = request.POST.get("change_status_list")
            list_ = True
        else:
            task_id = None

        task = Task.objects.get(id=task_id)
        if task.done:
            task.done = False
        else:
            task.done = True
        task.save()
        if list_:
            return redirect("/tasks_list/")
        else:
            return redirect(f"/tasks_list/{task_id}")
    return render(request, 'tasks_list.html', {})


def sort_tasks(request):
    pass


@login_required(login_url='/user_login/')
def delete_task(request):
    if request.method == "POST":
        task_id = request.POST["delete_task"]
        task = Task.objects.get(id=task_id)
        print("TASK", task)
        task.delete()
        return redirect(f"/tasks_list/")
    return render(request, 'tasks_list.html', {})


@login_required(login_url='/user_login/')
def update_task(request, task_id):
    if request.method == "POST":
        task = Task.objects.get(id=task_id)
        task.name = request.POST.get("name")
        task.category = request.POST.get("category")
        task.info = request.POST.get("info")
        task.description = request.POST.get("description")
        task.priority = request.POST.get("priority")

        start_data = request.POST.get("start_data")
        if start_data == "":
            pass
        else:
            task.end_data = start_data

        end_data = request.POST.get("end_data")
        if end_data == "":
            pass
        else:
            task.end_data = end_data
        task.save()
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
