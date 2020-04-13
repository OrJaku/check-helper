from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import datetime
from datetime import timedelta
from .models import Notes


@login_required(login_url='/user_login/')
def notes_list(request, *args, **kwargs):

    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        time = datetime.datetime.now() + timedelta(hours=2)
        time = time.strftime('%H:%M')
        new_note = Notes.objects.create(
            name=name,
            description=description,
            user=request.user,
            time=time,
            )
        new_note.save()
        return redirect("/notes_list/")
    date = Notes.objects.all().values('date').distinct().order_by('-date')
    days_str = []
    days_date = []
    for i in date:
        days_str.append(str(i['date']))
        days_date.append(i['date'])
    date = zip(days_str, days_date)
    from django.utils import timezone
    now = timezone.now()

    notes = Notes.objects.all().filter(user=request.user)

    context = {
        "notes": notes,
        "date": date,
    }
    return render(request, 'notes_list.html', context)


@login_required(login_url='/user_login/')
def delete_note(request):
    if request.method == "POST":
        note_id = request.POST["delete_note"]
        note = Notes.objects.get(id=note_id)
        messages.warning(request, f"Note {note.name} has been deleted")
        note.delete()
        return redirect(f"/notes_list/")
    return render(request, 'notes_list.html', {})

