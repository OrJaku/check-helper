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
        if name == "":
            messages.warning(request, "You need to add title to note")
            return redirect("/notes_list/")
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

    notes = Notes.objects.all().filter(user=request.user).order_by('-time')
    found_by_name = request.session.get('found_by_name')
    found_by_description = request.session.get('found_by_description')
    try:
        del request.session['found_by_name']
    except KeyError:
        found_by_name = None
    try:
        del request.session['found_by_description']
    except KeyError:
        found_by_description = None

    context = {
        "notes": notes,
        "date": date,
        "found_by_name": found_by_name,
        "found_by_description": found_by_description
    }
    return render(request, 'notes_list.html', context)


@login_required(login_url='/user_login/')
def delete_note(request):
    if request.method == "POST":
        note_id = request.POST["delete_note"]
        note = Notes.objects.get(id=note_id)
        messages.warning(request, f"Note {note.name} has been deleted")
        note.delete()
        return redirect("/notes_list/")
    return render(request, 'notes_list.html', {})


@login_required(login_url='/user_login/')
def searching_notes(request):
    if request.method == "POST":
        def search_function(search_sentences):
            notes_name = Notes.objects.filter(name__contains=search_sentences).filter(user=request.user)
            found_in_name = {}
            for note in notes_name:
                found_in_name[note.name] = [note.description, note.time, str(note.date)]
            notes_description = Notes.objects.filter(description__contains=search_sentences).filter(user=request.user)
            found_in_description = {}
            for note in notes_description:
                found_in_description[note.name] = [note.description, note.time, str(note.date)]
            return found_in_name, found_in_description
        search = request.POST["search"]
        if search == "":
            messages.info(request, "Fill searching window..")
            return redirect("/notes_list/")
        else:
            pass

        found_elements = search_function(search)
        if not found_elements[0] and not found_elements[1]:
            messages.warning(request, "No result found..")
        request.session["found_by_name"] = found_elements[0]
        request.session["found_by_description"] = found_elements[1]

        return redirect("/notes_list/")

    return render(request, 'notes_list.html', {{}})
