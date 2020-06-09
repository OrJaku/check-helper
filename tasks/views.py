from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Task, Brand, DailyTask
import datetime
import pytz
from datetime import timedelta


def date_function():
    time = datetime.datetime.today()
    tz = pytz.timezone('Europe/Warsaw')
    current_date = time.astimezone(tz)
    return current_date


def first_upper_letter(sentence):
    return sentence[:1].upper() + sentence[1:]


def daily_generator(current_date, user):
    tasks_daily_user = Task.objects.all().filter(user=user).filter(brand=2)
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

    daily_task_list_info = [name[0] for name in tasks_daily_user.values_list('info')]
    daily_task_list_name = [name[0] for name in tasks_daily_user.values_list('name')]
    daily_task_info = str(current_date)
    tasks_daily_settings = DailyTask.objects.all().filter(user=user)
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
                user,
                current_date,
                current_date,
                Brand.objects.get(id=2),
            ).save()
        else:
            pass


def spaces_remover(sentence):
    sentence = sentence.strip()
    sentence = sentence.replace('   ', ' ')
    sentence = sentence.replace('  ', ' ')
    return sentence


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
    name_task = spaces_remover(name_task)
    category_task = spaces_remover(category_task)
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


def categories(user):
    categories_list_tasks = Task.objects. \
        values_list('category'). \
        filter(user=user). \
        distinct(). \
        order_by('category')
    categories_list_tasks = [cat[0] for cat in categories_list_tasks]

    categories_list_daily_task = DailyTask.objects. \
        values_list('category'). \
        filter(user=user). \
        distinct(). \
        order_by('category')
    categories_list_daily_task = [cat[0] for cat in categories_list_daily_task]

    for cat in categories_list_daily_task:
        if cat not in categories_list_tasks:
            categories_list_tasks.append(cat)

    return categories_list_tasks


def home(request, *args, **kwargs):
    if request.user.is_authenticated:
        current_date = date_function().date()
        daily_generator(current_date, request.user)
        tasks = Task.objects.all().filter(user=request.user).order_by("done")
        tasks_days_lower_then_three = []
        tasks_today = []
        unique_categories = categories(request.user)

        for task in tasks:
            date_difference = task.end_data - current_date
            if 0 < date_difference.days <= 3:
                tasks_days_lower_then_three.append(task)
            elif date_difference.days == 0:
                tasks_today.append(task)
            else:
                pass
        context = {
            'tasks_days_lower_then_three': tasks_days_lower_then_three,
            'tasks_today': tasks_today,
            'unique_categories': unique_categories,
            }
        return render(request, 'home.html', context)
    return render(request, 'home.html', {})


@login_required(login_url='/user_login/')
def tasks_list(request):
    sort = "end_data"
    sort_archive = "-end_data"
    current_date = date_function().date()
    unique_categories = categories(request.user)
    filtering_categories = categories(request.user)
    daily_generator(current_date, request.user)

    if request.method == "POST":
        if "daily" in request.POST:
            if len(DailyTask.objects.all().filter(user=request.user)) >= 8:
                messages.error(request, f"You can not have more then 8 daily tasks")
                return redirect('/tasks_list/')
            else:
                pass
            name = request.POST.get("name")
            if name == "":
                name = f"daily_{date_function().strftime('%H%M%S')}"
                messages.warning(request, f"Daily task name generated automatically: {name}")
            category = request.POST.get("category")
            if category == "" or category is None:
                if "category_select" in request.POST:
                    category = request.POST.get("category_select")
                else:
                    messages.warning(request, f"Yoy have to choose category")
                    return redirect('/tasks_list/')
            else:
                pass

            description = request.POST.get("description")
            name = spaces_remover(name)
            category = spaces_remover(category)
            category = first_upper_letter(category)
            daily_task = DailyTask.objects.create(
                name=name,
                category=category,
                description=description,
                user=request.user,
            )
            daily_task.save()
            messages.success(request, f"New daily task '{name}' has been added ")
            return redirect("/tasks_list/")

        elif "sort" in request.POST:
            sort = request.POST.get("sort")
            if sort[0] == "-":
                print(sort[0])
                pass
            else:
                sort = "" + sort

        elif "add" in request.POST:
            if len(Task.objects.all().filter(user=request.user)) >= 150:
                messages.error(request, f"You can not have more then 150 tasks")
                return redirect('/tasks_list/')
            else:
                pass
            home_ = False
            if 'home' in request.POST.get("add"):
                home_ = True
            name = request.POST.get("name")
            category = request.POST.get("category")
            if category == "" or category is None or name == "" or name is None:
                if request.POST.get("category_select") == ".. or choose category":
                    messages.warning(request, f"Yoy have to add name andgit  choose category")
                    if home_ is False:
                        return redirect('/tasks_list/')
                    else:
                        return redirect('/')
                else:
                    category = request.POST.get("category_select")
            else:
                pass
            category = first_upper_letter(category)
            info = request.POST.get("info")
            description = request.POST.get("description")
            priority = request.POST.get("priority")
            start_data = request.POST.get("start_data")
            if start_data == "" or start_data is None:
                start_data = current_date
            else:
                pass
            try:
                delta = int(request.POST.get("delta"))
            except (ValueError, TypeError):
                delta = ""

            if delta == "" or delta is None:
                delta = 10
            else:
                pass

            end_data = request.POST.get("end_data")
            if end_data == "" or end_data is None:
                end_data = current_date + timedelta(delta)
            else:
                pass
            if priority == "" or priority is None:
                priority = 1
            else:
                pass
            if name == "" and category == "" and info == "" and description == "":
                messages.warning(request, f"You did not fill task data")
                return redirect("/tasks_list/")
            elif name == "":
                name = f"New task {date_function().strftime('%H:%M:%S')}"
            else:
                pass

            new_task(name, category, info, description, priority, request.user, start_data, end_data).save()
            messages.success(request, f"New task '{name}' has been added ")
            if home_ is False:
                return redirect('/tasks_list/')
            else:
                return redirect('/')
        elif "category" in request.POST:
            new_category = [request.POST.get("category")]

            if new_category[0] == "All":
                pass
            else:
                filtering_categories = new_category
        else:
            return render(request, 'tasks_list.html', {})

    daily_tasks_user = DailyTask.objects.all().filter(user=request.user)

    def zipping_daily(lists):
        date_difference_daily = []

        for task in lists:
            difference_daily = date_function().date() - task.first_date
            days1 = str(difference_daily).split(" ")
            try:
                days1 = int(days1[0]) + 1
            except ValueError:
                days1 = 1
            date_difference_daily.append(days1)
        zipped_list_d = zip(lists, date_difference_daily)
        return zipped_list_d

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

    daily_tasks_user_with_completed_days = zipping_daily(daily_tasks_user)
    tasks_user = Task.objects.all().filter(user=request.user). \
        filter(brand=1). \
        filter(category__in=filtering_categories)

    tasks_daily_user = Task.objects.all(). \
        filter(user=request.user).filter(brand=2). \
        filter(category__in=filtering_categories)

    tasks_user_archive = Task.objects.all(). \
        filter(user=request.user). \
        filter(category__in=filtering_categories)

    tasks_user_with_date_difference = zipping(tasks_user.order_by(sort))
    tasks_user_archive_with_date_difference = zipping(tasks_user_archive.order_by(sort_archive))
    tasks_daily_user_with_date_difference = zipping(tasks_daily_user.order_by(sort))

    found_elements = request.session.get('found_elements')
    try:
        del request.session['found_elements']
    except KeyError:
        found_elements = None

    context = {
        'tasks': tasks_user_with_date_difference,
        'tasks_archive': tasks_user_archive_with_date_difference,
        'tasks_daily': tasks_daily_user_with_date_difference,
        'daily_tasks_user_with_completed_days': daily_tasks_user_with_completed_days,
        'found_elements': found_elements,
        'unique_categories': unique_categories,
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
        home_ = False
        if "change_status" in request.POST:
            task_id = request.POST.get("change_status")
        elif "change_status_list" in request.POST:
            task_id = request.POST.get("change_status_list")
            list_ = True
        elif "change_status_home" in request.POST:
            task_id = request.POST.get("change_status_home")
            home_ = True
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
        elif home_:
            return redirect("/")
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
        name = request.POST.get("name")
        name = spaces_remover(name)
        task.name = name
        category = request.POST.get("category")
        category = spaces_remover(category)
        task.category = category
        task.info = request.POST.get("info")
        task.description = request.POST.get("description")
        share = request.POST.get("share")
        if share == "" or share is None:
            print(task.share)
            task.share.username = 'kuba'
            print(task.share.username)
            print(task.share)
        priority = request.POST.get("priority")
        if priority == "" or priority is None:
            task.priority = 1
        else:
            pass
        start_data = request.POST.get("start_data")
        if start_data == "" or start_data is None:
            pass
        else:
            task.end_data = start_data

        end_data = request.POST.get("end_data")
        print(end_data)
        if end_data == "" or end_data is None:
            pass
        else:
            task.end_data = end_data
        print(task.share)
        task.save()
        print(task.share)
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
        messages.warning(request, f"Daily task {daily_task.name} has been deleted")
        return redirect(f"/tasks_list/")
    return render(request, 'tasks_list.html', {})


@login_required(login_url='/user_login/')
def searching_tasks(request):
    if request.method == "POST":
        def search_function(search_sentences):
            found_tasks = {}

            def task_finder(tasks):
                for task in tasks:
                    found_tasks[task.name] = [task.id,
                                              task.info,
                                              task.category,
                                              task.description,
                                              str(task.end_data),
                                              str(task.start_data),
                                              str(task.brand),
                                              task.done,
                                              ]
                return found_tasks
            tasks_name = Task.objects.filter(name__contains=search_sentences).filter(user=request.user)
            tasks_description = Task.objects.filter(description__contains=search_sentences) \
                .filter(user=request.user) \
                .order_by("name")
            tasks_info = Task.objects.filter(info__contains=search_sentences) \
                .filter(user=request.user) \
                .order_by("name")
            tasks_category = Task.objects.filter(category__contains=search_sentences) \
                .filter(user=request.user) \
                .order_by("name")
            found_tasks = task_finder(tasks_name)
            found_tasks = task_finder(tasks_description)
            found_tasks = task_finder(tasks_info)
            found_tasks = task_finder(tasks_category)
            return found_tasks

        search = request.POST["search"]
        if search == "":
            messages.info(request, "Fill searching window..")
            return redirect("/tasks_list/")
        else:
            pass
        found_elements = search_function(search)
        if not found_elements:
            messages.warning(request, "No result found..")
        request.session["found_elements"] = found_elements
        return redirect("/tasks_list/")
    return render(request, 'tasks_list.html', {{}})


def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Login success as user: {username}')
            return redirect('/')
        else:
            messages.error(request, 'Invalid login or password')
        return render(request, 'user_login.html', {})
    else:
        return render(request, 'user_login.html', {})


def user_logout(request):
    logout(request)
    messages.info(request, 'You are logged out')
    return redirect('/')
