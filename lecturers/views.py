from django.shortcuts import render, get_object_or_404, redirect
from .models import LecturerInfo
from django.contrib.auth.models import User 
from .forms import CreateLecturer
from django.contrib import messages
from django.core.paginator import Paginator
from .forms import SignUpForm , SessionForm
from django.contrib.auth import login
from students.models import *
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
    if request.user.is_authenticated:
        students = StudentInfo.objects.all()
        lecturers=LecturerInfo.objects.all()
        
        try:
            logged_in_as_student = StudentInfo.objects.get(name= request.user)
        except:
            logged_in_as_student = ""
           
            
        try:
            logged_in_as_lecturer = LecturerInfo.objects.get(name= request.user)
        except:
            logged_in_as_lecturer=""
    context = {
        "single_lecturer": single_lecturer,
          "logged_in_as_student":logged_in_as_student,
        "logged_in_as_lecturer": logged_in_as_lecturer,
        "students":students,
        "lecturers":lecturers
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
    return render(request, "lecturers/create_lecturer.html", context)


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
    return render(request, "lectures/edit_lecturer.html", context)


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
            lecturerProfiles = LecturerInfo.objects.create( name = users , lecturer_email=users.email,full_name=users.get_full_name())
            lecturerProfiles.save()

            new_user.save()
          
            login(request, new_user)
            return redirect('home')
    context = {'form': form}
    return render(request, 'lecturers/registration/register.html', context)


def session(request):
    if request.method == "POST":
        form = SessionForm(request.POST)

        if form.is_valid():
            form.save()
        messages.success(request, "Session created Successfully!")
        return redirect("home")
    else:
        form = SessionForm()

    context = {'form': form}
    return render(request, "lecturers/session.html" , context  )

def single_session(request, session_id):
    session = StudentSession.objects.get(id=session_id)
    context = {"session":session}
    return render(request,"lecturers/single_session.html",context)