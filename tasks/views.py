from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
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
                                    )
        new_task.save()
        return redirect('/tasks_list/')

    tasks = Task.objects.all()
    context = {
        'objects': tasks,
        'status': "table-success"
    }
    return render(request, 'tasks_list.html', context)


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




