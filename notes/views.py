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

    notes = Notes.objects.all().filter(user=request.user)
    context = {
        "notes": notes,
    }
    return render(request, 'notes_list.html', context)

