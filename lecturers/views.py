from django.shortcuts import render, get_object_or_404, redirect
from .models import LecturerInfo
from django.contrib.auth.models import User 
from .forms import CreateLecturer
from django.contrib import messages
from django.core.paginator import Paginator
from .forms import SignUpForm
from django.contrib.auth import login

# Create your views here.
def lecturer_list(request):
    lecturers = LecturerInfo.objects.all()

    paginator = Paginator(lecturers, 10)
    page = request.GET.get('page')
    paged_lecturers = paginator.get_page(page)
    context = {
        "lecturers": paged_lecturers
    }
    return render(request, "lecturers/lecturer_list.html", context)


def single_lecturer(request, lecturer_id):
    single_lecturer = get_object_or_404(LecturerInfo, pk=lecturer_id)
    context = {
        "single_lecturer": single_lecturer
    }
    return render(request, "lecturers/single_lecturer.html", context)


def create_lecturer(request):
    if request.method == "POST":
        forms = CreateLecturer(request.POST, request.FILES or None)

        if forms.is_valid():
            forms.save()
        messages.success(request, "Lecturer Registration Successfully!")
        return redirect("lecturers:lecturer_list")
    else:
        forms = CreateLecturer()

    context = {
        "forms": forms
    }
    return render(request, "lecturers/create_lecturers.html", context)


def edit_lecturer(request, pk):
    lecturer_edit = LecturerInfo.objects.get(id=pk)
    edit_lecturer_forms = CreateLecturer(instance=lecturer_edit)

    if request.method == "POST":
        edit_lecturer_forms = CreateLecturer(request.POST, request.FILES or None, instance=lecturer_edit)

        if edit_lecturer_forms.is_valid():
            edit_lecturer_forms.save()
            messages.success(request, "Edit Lecturer Info Successfully!")
            return redirect("lecturers:lecturer_list")

    context = {
        "edit_lecturer_forms": edit_lecturer_forms
    }
    return render(request, "lecturers/edit_lecturer.html", context)


def delete_lecturer(request, lecturer_id):
    lecturer_delete = LecturerInfo.objects.get(id=lecturer_id)
    lecturer_delete.delete()
    messages.success(request, "Delete Lecturer Info Successfully")
    return redirect("lecturers:lecturer_list")


def register(request):
 
    if request.method != 'POST':
        # Display blank registration form. 
        form = SignUpForm()
    else:
        # Process completed form.
        form = SignUpForm(data=request.POST)
        
        if form.is_valid():
            new_user = form.save()
            get_id = form.instance.id  # get the id of a use--it has a username inside
            users = User.objects.get(id=get_id) # get the new user
            print(users)
            lecturerProfiles = LecturerInfo.objects.create( name = users)
            lecturerProfiles.save()

            new_user.save()
          
            login(request, new_user)
            return redirect('home')
    context = {'form': form}
    return render(request, 'lecturers/registration/register.html', context)

