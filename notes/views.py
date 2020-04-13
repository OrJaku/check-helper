from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Notes


@login_required(login_url='/user_login/')
def notes_list(request, *args, **kwargs):

    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        new_note = Notes.objects.create(
            name=name,
            description=description,
            user=request.user
            )
        new_note.save()
        return redirect("/notes_list/")
    date = Notes.objects.all().values('date').distinct().order_by('-date')
    days = []
    for i in date:
        days.append(i['date'])

    notes = Notes.objects.all().filter(user=request.user)

    context = {
        "days": days,
        "notes": notes,
    }
    return render(request, 'notes_list.html', context)

