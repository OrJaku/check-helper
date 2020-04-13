from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Task, Brand, DailyTask
import datetime
from datetime import timedelta


def home(request, *args, **kwargs):
    print(request.user)

    return render(request, 'home.html', {})


@login_required(login_url='/user_login/')
def tasks_list(request):

    def new_task(
            name_task,
            category_task,
            info_task,
            description_task,
            priority_task,
            user,
            start_data_task,
            end_data_task,
            brand=Brand.objects.get(id=1),
            ):
        task = Task.objects.create(
                                name=name_task,
                                category=category_task,
                                info=info_task,
                                description=description_task,
                                start_data=start_data_task,
                                end_data=end_data_task,
                                priority=priority_task,
                                brand=brand,
                                user=user,
                                )
        return task

    sort = "end_data"
    sort_archive = "-end_data"

    current_date = datetime.date.today()

    tasks_user = Task.objects.all().filter(user=request.user).filter(brand=1)
    tasks_daily_user = Task.objects.all().filter(user=request.user).filter(brand=2)

    for task_daily_user in tasks_daily_user:
        difference = task_daily_user.end_data - current_date
        days = str(difference).split(" ")
        try:
            days = int(days[0])
        except ValueError:
            days = 0
        if days < 0:
            if task_daily_user.done is True and task_daily_user.brand.id == 2:
                try:
                    daily_task_completed = DailyTask.objects.get(name=task_daily_user.name)
                    daily_task_completed.completed += 1
                    daily_task_completed.save()
                except DailyTask.DoesNotExist:
                    print(f'{task_daily_user} does not exist')
            else:
                pass
            task_daily_user.delete()
        else:
            pass

    tasks_user_archive = Task.objects.all().filter(user=request.user)

    daily_task_list_info = [name[0] for name in tasks_daily_user.values_list('info')]
    daily_task_list_name = [name[0] for name in tasks_daily_user.values_list('name')]

    daily_task_info = str(current_date)

    tasks_daily_settings = DailyTask.objects.all().filter(user=request.user)

    for task_daily_settings in tasks_daily_settings:
        if daily_task_info not in daily_task_list_info or task_daily_settings.name not in daily_task_list_name:
            daily_task = DailyTask.objects.get(id=task_daily_settings.id)
            if daily_task.name == "":
                name = "Empty"
            else:
                name = daily_task.name
            new_task(
                name,
                daily_task.category,
                daily_task_info,
                daily_task.description,
                1,
                request.user,
                current_date,
                current_date,
                Brand.objects.get(id=2),
                ).save()
        else:
            pass

    if request.method == "POST":
        if "daily" in request.POST:
            tag = request.POST.get("tag")
            name = request.POST.get("name")
            if tag == "" or name == "":
                messages.warning(request, f"You have to add tag and name of daily task")
                return redirect("/tasks_list/")
            category = request.POST.get("category")
            description = request.POST.get("description")
            daily_task = DailyTask.objects.create(
                tag=tag,
                name=name,
                category=category,
                description=description,
                user=request.user,
            )
            daily_task.save()
            messages.success(request, f"New daily task '{tag}' has been added ")

            return redirect("/tasks_list/")

        elif "sort" in request.POST:
            sort = request.POST.get("sort")
            if sort[0] == "-":
                print(sort[0])
                pass
            else:
                sort = "" + sort

        elif "add" in request.POST:

            name = request.POST.get("name")

            category = request.POST.get("category")
            category = category.title()

            info = request.POST.get("info")

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
            if name == "" and category == "" and info == "" and description == "":
                messages.warning(request, f"You did not fill task data")
                return redirect("/tasks_list/")
            elif name == "":
                name = f"New task {datetime.datetime.now().strftime('%H:%M:%S')}"
            else:
                pass

            new_task(name, category, info, description, priority, request.user, start_data, end_data).save()
            messages.success(request, f"New task '{name}' has been added ")
            return redirect('/tasks_list/')

        else:
            return render(request, 'tasks_list.html', {})

    daily_tasks_user = DailyTask.objects.all().filter(user=request.user)

    def zipping_daily(lists):
        date_difference1 = []

        for task in lists:
            difference1 = datetime.date.today() - task.first_date
            days1 = str(difference1).split(" ")
            try:
                days1 = int(days1[0]) + 1
            except ValueError:
                days1 = 1
            date_difference1.append(days1)
        zipped_list_d = zip(lists, date_difference1)
        return zipped_list_d

    daily_tasks_user_with_completed_days = zipping_daily(daily_tasks_user)

    def zipping(lists):
        date_difference = []

        for task in lists:
            difference_days = task.end_data - current_date
            numbers_days = str(difference_days).split(" ")
            try:
                numbers_days = int(numbers_days[0])
            except ValueError:
                numbers_days = 0
            date_difference.append(numbers_days)
        zipped_list = zip(lists, date_difference)
        return zipped_list

    tasks_user_with_date_difference = zipping(tasks_user.order_by(sort))
    tasks_user_archive_with_date_difference = zipping(tasks_user_archive.order_by(sort_archive))
    tasks_daily_user_with_date_difference = zipping(tasks_daily_user.order_by(sort))

    context = {
        'tasks': tasks_user_with_date_difference,
        'tasks_archive': tasks_user_archive_with_date_difference,
        'tasks_daily': tasks_daily_user_with_date_difference,
        "daily_tasks_user_with_completed_days": daily_tasks_user_with_completed_days,

    }
    return render(request, 'tasks_list.html', context)


@login_required(login_url='/user_login/')
def task_detail(request, task_id):
    try:
        task = Task.objects.get(id=task_id)
        context = {
            'task': task,
        }
        return render(request, 'task_detail.html', context)

    except Task.DoesNotExist:
        context = {}
        return render(request, 'home.html', context)


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


@login_required(login_url='/user_login/')
def delete_task(request):
    if request.method == "POST":
        task_id = request.POST["delete_task"]
        task = Task.objects.get(id=task_id)
        task.delete()
        messages.warning(request, f"Task {task.name} has been deleted")
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
        messages.info(request, f"Task {task.name} updated")
        return redirect(f'/tasks_list/{task_id}')
    return render(request, 'tasks_list.html', {})


def daily_tasks_settings(request):
    return render(request, 'home.html', {})


@login_required(login_url='/user_login/')
def delete_daily_task(request):
    if request.method == "POST":
        task_id = request.POST["delete_daily_task"]
        daily_task = DailyTask.objects.get(id=task_id)
        daily_task.delete()
        messages.warning(request, f"Daily task {daily_task.tag} has been deleted")
        return redirect(f"/tasks_list/")
    return render(request, 'tasks_list.html', {})


def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Login success as user: {username}')
            return redirect('/tasks_list/')
        else:
            messages.error(request, 'Invalid login or password')
        return render(request, 'home.html', {})
    else:
        return render(request, 'user_login.html', {})


def user_logout(request):
    logout(request)
    messages.info(request, 'You are logged out')
    return redirect('/')

