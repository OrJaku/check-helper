from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import datetime
import pytz
from .models import Notes


def date_function():
    time = datetime.datetime.today()
    tz = pytz.timezone('Europe/Warsaw')
    current_date = time.astimezone(tz)
    return current_date


@login_required(login_url='/user_login/')
def notes_list(request, *args, **kwargs):
    current_full_date = date_function()
    current_month = current_full_date.strftime('%B')
    current_year = int(current_full_date.strftime('%Y'))
    auto_name = current_full_date.strftime('%H:%M:%S')
    if request.method == "POST":
        name = request.POST.get("name")
        if name == "" or name == " " or name == "  ":
            name = f"Note {auto_name}"
        description = request.POST.get("description")
        if description == "" or description == " " or description == "  ":
            messages.warning(request, f"You did not file note")
            return redirect("/notes_list/")
        tag = request.POST.get("tag")
        if tag == "" or tag == " " or tag == "  ":
            tag = "NoTag"
        new_note = Notes.objects.create(
            name=name,
            description=description,
            user=request.user,
            tag=tag,
            time=current_full_date.strftime('%H:%M'),
            )
        new_note.save()
        return redirect("/notes_list/")
    date_db = Notes.objects.all().filter(user=request.user).values('date').distinct().order_by('-date')
    days_str = []
    days_date = []
    month_date = []
    year_date = []
    existing_month_list = []
    existing_month_name_list = []
    months_list = [
                    "Unknown",
                    "January",
                    "February",
                    "March",
                    "April",
                    "May",
                    "June",
                    "July",
                    "August",
                    "September",
                    "October",
                    "November",
                    "December",
                    ]
    for i in date_db:
        days_str.append(str(i['date']))
        days_date.append(i['date'])
        month_date.append(i['date'].month)
        year_date.append(i['date'].year)
        if i['date'].month in existing_month_list:
            pass
        else:
            existing_month_list.append(i['date'].month)
            existing_month_name_list.append(months_list[i['date'].month])

    date = zip(days_str, days_date, month_date)
    date_previous_years = set(year_date)
    date_month = zip(existing_month_list, existing_month_name_list)

    notes = Notes.objects.all().filter(user=request.user).order_by('-date')
    # Searching
    founds_list = []
    found_by_name = request.session.get('found_by_name')
    found_by_description = request.session.get('found_by_description')
    found_by_tag = request.session.get('found_by_tag')
    try:
        del request.session['found_by_name']
    except KeyError:
        found_by_name = None
    try:
        del request.session['found_by_description']
    except KeyError:
        found_by_description = None
    try:
        del request.session['found_by_tag']
    except KeyError:
        found_by_tag = None
    auto_name = current_full_date.strftime('%H:%M:%S')
    founds_list.append(found_by_name)
    founds_list.append(found_by_description)
    founds_list.append(found_by_tag)
    founds_list_enumerate = enumerate(founds_list)

    unique_tags = Notes.objects.values_list('tag').filter(user=request.user).distinct()
    unique_tags = [tag[0] for tag in unique_tags]

    context = {
        "notes": notes,
        "date": date,
        "date_previous_years": date_previous_years,
        "founds_list_enumerate": founds_list_enumerate,
        "auto_name": auto_name,
        "unique_tags": unique_tags,
        "current_full_date": current_full_date,
        "date_month": date_month,
        "current_month": current_month,
        "current_year": current_year,
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


def tag_list(request, tag):
    notes_by_tag = Notes.objects.all().filter(tag=tag)
    context = {
        "tag": tag,
        "notes_by_tag": notes_by_tag,
    }
    return render(request, 'tag_list.html', context)


@login_required(login_url='/user_login/')
def update_note(request, note_id):
    if request.method == "POST":
        note = Notes.objects.get(id=note_id)
        note.name = request.POST.get('name')
        note.tag = request.POST.get('tag')
        note.description = request.POST.get('description')
        note.save()
        messages.info(request, f"Note {note.name} updated")
        return redirect(f'/notes_list/{note_id}')
    return render(request, 'notes_list.html', {})


@login_required(login_url='/user_login/')
def note_detail(request, note_id):
    try:
        note = Notes.objects.get(id=note_id)
        context = {
            'note': note,
        }
        return render(request, 'note_detail.html', context)

    except Notes.DoesNotExist:
        context = {}
        return render(request, 'home.html', context)


@login_required(login_url='/user_login/')
def searching_notes(request):
    if request.method == "POST":
        def search_function(search_sentences):
            notes_name = Notes.objects.filter(name__contains=search_sentences).filter(user=request.user)
            found_in_name = {}
            for note in notes_name:
                found_in_name[note.name] = [
                                            note.description,
                                            note.time,
                                            str(note.date),
                                            note.tag,
                                            note.id,
                                            ]
            notes_description = Notes.objects.filter(description__contains=search_sentences).filter(user=request.user)
            found_in_description = {}
            for note in notes_description:
                found_in_description[note.name] = [
                                                    note.description,
                                                    note.time,
                                                    str(note.date),
                                                    note.tag,
                                                    note.id,
                                                    ]
            notes_tag = Notes.objects.filter(tag__contains=search_sentences).filter(user=request.user)
            found_in_tag = {}
            for note in notes_tag:
                found_in_tag[note.name] = [
                                            note.description,
                                            note.time,
                                            str(note.date),
                                            note.tag,
                                            note.id,
                                            ]
            return found_in_name, found_in_description, found_in_tag
        search = request.POST["search"]
        if search == "":
            messages.info(request, "Fill searching window..")
            return redirect("/notes_list/")
        else:
            pass

        found_elements = search_function(search)
        if not found_elements[0] and not found_elements[1] and not found_elements[2]:
            messages.warning(request, "No result found..")
        request.session["found_by_name"] = found_elements[0]
        request.session["found_by_description"] = found_elements[1]
        request.session["found_by_tag"] = found_elements[2]

        return redirect("/notes_list/")

    return render(request, 'notes_list.html', {{}})
