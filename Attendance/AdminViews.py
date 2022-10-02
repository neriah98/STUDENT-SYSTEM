from urllib import request
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage #To upload Profile Picture
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Attendance, CustomUser ,Modules,Lecturers, Courses ,Students ,Sessions, Venues
from .forms import AddStudentForm ,EditStudentForm



def admin_home(request):
    #Counts
    
    total_lectures_count = Lecturers.objects.all().count()
    total_students_count = Students.objects.all().count()
    total_course_count = Courses.objects.all().count()
    total_modules_count = Modules.objects.all().count()
   
    
    
    #Total Modules and Students in each course
    course_all =Courses.objects.all()
    course_name_list =[]
    module_count_list =[]
    student_count_list_in_course =[]

    for course in course_all:
        modules = Modules.objects.filter(course_id =course.id).count()
        students =Students.objects.filter(course_id=course.id).count()
        course_name_list.append(modules)
        student_count_list_in_course.append(students)

        module_all  = Modules.objects.all()
        module_list =[]
        student_count_list_in_module =[]

        for module in module_all:
            course =Courses.objects.get(id =module.course_id.id)
            student_count =Students.objects.filter(course_id=course.id).count()
            module_list.append(module.module_description)
            student_count_list_in_module.append(student_count)

       #For Lecturer in each module
        # lecturer_name_list =[]
        # lecturers =Lecturer.objects.all()

        # for lecturer in lecturers:
        #     module_ids = Module.objects.filter(lecturer_id=lecturer.user.id)
        #     lecturer_name_list.append(lecturer.user.last_name)



    context={
        "all_student_count": total_students_count,
        "module_count": total_modules_count,
        "lecturer_count": total_lectures_count,
        "course_count" :total_course_count,
        "course_name_list":course_name_list,
        "module_count_list": module_count_list,
       # "student_count_list_in_course":student_count_list_in_course,
        #"module_list": module_list,
        #"student_count_list_in_module": student_count_list_in_module,
       
    
    }
    return render(request, "admin_template/admin_home.html", context)
 


def add_lecturer(request):
    return render(request, "admin_template/add_lecturer_template.html")
 
 
def add_lecturer_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method ")
        return redirect('add_lecturer')
    else:
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        contact_number = request.POST.get('contact_number')
        office_number = request.POST.get('office_number')
        
 
        try:
            user= CustomUser.objects.create_user(email=email,
                                                  username=username,
                                                  password=password,
                                                  first_name=first_name,
                                                  last_name=last_name,
                                                  contact_number = contact_number,
                                                  user_role=2)
            user.lecturers.office_number = office_number
            user.save()
            messages.success(request, "Lecturer Added Successfully!")
            return redirect('add_lecturer')
        except:
            messages.error(request, "Failed to Add Lecturer!")
            return redirect('add_lecturer')
 
 
 
def manage_lecturer(request):
    lecturers = Lecturers.objects.all()
    context = {
        "lecturers": lecturers
    }
    return render(request, "admin_template/manage_lecturer_template.html", context)
 
 
def edit_lecturer(request, lecturer_id):
    lecturer = Lecturers.objects.get(user=lecturer_id)
 
    context = {
        "lecturer": lecturer,
        "id": lecturer_id
    }
    return render(request, "admin_template/edit_lecturer_template.html", context)
 
 
def edit_lecturer_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        lecturer_id = request.POST.get('lecturer_id')
        email = request.POST.get('email')
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        contact_number = request.POST.get('contact_number')
        office_number = request.POST.get('office_number')
        
 
        try:
            # INSERTING into Customuser Model
            user = CustomUser.objects.get(id=lecturer_id)
            user.email = email
            user.username = username
            user.first_name = first_name
            user.last_name = last_name
            user.contact_number =contact_number
            user.save()
             
            # INSERTING into Staff Model
            lecturer_model = Lecturers.objects.get(user=lecturer_id)
            lecturer_model.office_number = office_number
            lecturer_model.save()
 
            messages.success(request, "Lecturer Updated Successfully.")
            return redirect('/edit_lecturer/'+lecturer_id)
 
        except:
            messages.error(request, "Failed to Update Lecturer.")
            return redirect('/edit_lecturer/'+lecturer_id)
 
 
 
def delete_lecturer(request, lecturer_id):
    lecturer = Lecturers.objects.get(user=lecturer_id)
    try:
        lecturer.delete()
        messages.success(request, "Lecturer Deleted Successfully.")
        return redirect('manage_lecturer')
    except:
        messages.error(request, "Failed to Delete Lecturer.")
        return redirect('manage_lecturer') 
def add_course(request):
    return render(request, "admin_template/add_course_template.html")


def add_course_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('add_course')
    else:
        course = request.POST.get('course')
        try:
            course_model = Courses(course_name=course)
            course_model.save()
            messages.success(request, "Course Added Successfully!")
            return redirect('add_course')
        except:
            messages.error(request, "Failed to Add Course!")
            return redirect('add_course')


def manage_course(request):
    courses = Courses.objects.all()
    context = {
        "courses": courses
    }
    return render(request, 'admin_template/manage_course_template.html', context)


def edit_course(request, course_id):
    course = Courses.objects.get(id=course_id)
    context = {
        "course": course,
        "id": course_id
    }
    return render(request, 'admin_template/edit_course_template.html', context)


def edit_course_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method")
    else:
        course_id = request.POST.get('course_id')
        course_name = request.POST.get('course')

        try:
            course = Courses.objects.get(id=course_id)
            course.course_name = course_name
            course.save()

            messages.success(request, "Course Updated Successfully.")
            return redirect('/edit_course/'+course_id)

        except:
            messages.error(request, "Failed to Update Course.")
            return redirect('/edit_course/'+course_id)


def delete_course(request, course_id):
    course = Courses.objects.get(id=course_id)
    try:
        course.delete()
        messages.success(request, "Course Deleted Successfully.")
        return redirect('manage_course')
    except:
        messages.error(request, "Failed to Delete Course.")
        return redirect('manage_course')


#Venue
# def add_venue(request):
#     return render(request, "admin_template/add_venue_template.html")


# def add_venue_save(request):
#     if request.method != "POST":
#         messages.error(request, "Invalid Method!")
#         return redirect('add_venue')
#     else:
#         venue = request.POST.get('venue')
#         try:
#             venue_model = Venues(venue_name=venue)
#             venue_model.save()
#             messages.success(request, "Venue Added Successfully!")
#             return redirect('add_venue')
#         except:
#             messages.error(request, "Failed to Add Venue!")
#             return redirect('add_venue')


# def manage_venue(request):
#     venues = Venues.objects.all()
#     context = {
#         "venues": venues
#     }
#     return render(request, 'admin_template/manage_venue_template.html', context)


# def edit_venue(request, venue_id):
#     venue = Venues.objects.get(id=venue_id)
#     context = {
#         "venue": venue,
#         "id": venue_id
#     }
#     return render(request, 'admin_template/edit_venue_template.html', context)


# def edit_venue_save(request):
#     if request.method != "POST":
#         HttpResponse("Invalid Method")
#     else:
#         venue_id = request.POST.get('venue_id')
#         venue_name = request.POST.get('venue')

#         try:
#             venue = Venues.objects.get(id=venue_id)
#             venue.venue_name = venue_name
#             venue.save()

#             messages.success(request, "Venue Updated Successfully.")
#             return redirect('/edit_venue/'+venue_id)

#         except:
#             messages.error(request, "Failed to Update Venue.")
#             return redirect('/edit_venue/'+venue_id)


# def delete_venue(request, venue_id):
#     venue = Venues.objects.get(id=venue_id)
#     try:
#         venue.delete()
#         messages.success(request, "Venue Deleted Successfully.")
#         return redirect('manage_venue')
#     except:
#         messages.error(request, "Failed to Delete Venue.")
#         return redirect('manage_venue')



def manage_session(request):
    sessions = Sessions.objects.all()
    context = {
        "sessions": sessions
    }
    return render(request, "admin_template/manage_session_template.html", context)


def add_session(request):
    return render(request, "admin_template/add_session_template.html")


def add_session_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('add_course')
    else:
        session_name= request.POST.get('session_name')
        session_date =request.POST.get('session_date')
        session_time =request.POST.get('session_time')

        # venue_id = request.POST.get('venue')
        # venue = Venues.objects.get(id=venue_id)
 

        try:
            session= Sessions(session_name=session_name, session_date=session_date ,session_time=session_time)
            session.save()
            messages.success(request, "Session  added Successfully!")
            return redirect("add_session")
        except:
            messages.error(request, "Failed to Add Session Year")
            return redirect("add_session")


def edit_session(request, session_id):
    session = Sessions.objects.get(id=session_id)
    context = {
        "session": session

    }
    return render(request, "admin_template/edit_session_template.html", context)


def edit_session_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('manage_session')
    else:
        session_id = request.POST.get('session_id')
        session_name= request.POST.get('session_name')
        session_date =request.POST.get('session_date')
        session_time =request.POST.get('session_time')

        # venue_id = request.POST.get('venue')

        try:
            session = Sessions.objects.get(id=session_id)
            session.session_name = session_name
            session.session_date= session_date
            session.session_time= session_time

            # venue = Venues.objects.get(id=venue_id)
            # session.venue_id = venue


            session.save()

            messages.success(request, "Session  Updated Successfully.")
            return redirect('/edit_session/'+session_id)
        except:
            messages.error(request, "Failed to Update Session .")
            return redirect('/edit_session/'+session_id)


def delete_session(request, session_id):
    session = Sessions.objects.get(id=session_id)
    try:
        session.delete()
        messages.success(request, "Session Deleted Successfully.")
        return redirect('manage_session')
    except:
        messages.error(request, "Failed to Delete Session.")
        return redirect('manage_session')

def add_student(request):
    form = AddStudentForm()
    context = {
        "form": form
    }
    return render(request, 'admin_template/add_student_template.html', context)
 
 
 
def add_student_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('add_student')
    else:
        form = AddStudentForm(request.POST, request.FILES)
 
        if form.is_valid():
            #title = form.cleaned_data['title']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            contact_number = form.cleaned_data['contact_number']
            student_number = form.cleaned_data['student_number']
            course_id = form.cleaned_data['course_id']
            session_id = form.cleaned_data['session_id']
            password = form.cleaned_data['password']

 
             
            if len(request.FILES) != 0:
                profile_pic = request.FILES['profile_pic']
                file= FileSystemStorage()
                filename = file.save(profile_pic.name, profile_pic)
                profile_pic_url = file.url(filename)
            else:
                profile_pic_url = None
 
 
            try:
                user = CustomUser.objects.create_user(#title =title,
                                                      first_name=first_name,
                                                      last_name=last_name,
                                                      username=username,
                                                      email=email,
                                                      contact_number=contact_number,
                                                      password=password,
                                                      user_role=3)
                user.students.student_number = student_number

                course = Courses.objects.get(id=course_id)
                user.students.course_id = course

                session = Sessions.objects.get(id=session_id)
                user.students.session_id = session
 
               #.objects.get(id= module_enrollment_id)
                #user.student. module_enrollment_id = module_enrollemnt_obj
 
 
              
                user.students.profile_pic = profile_pic_url
                user.save()
                messages.success(request, "Student Added Successfully!")
                return redirect('add_student')
            except:
                messages.error(request, "Failed to Add Student!")
                return redirect('add_student')
        else:
            return redirect('add_student') 



def manage_student(request):
    students = Students.objects.all()
    context = {
        "students": students
    }
    return render(request, 'admin_template/manage_student_template.html', context)

 

def edit_student(request, student_id):
   
    # Adding Student ID into Session Variable
    request.session['student_id'] = student_id
 
    student = Students.objects.get(user=student_id)
    form = EditStudentForm()
     
    # Filling the form with Data from Database
    #form.fields['title'].initial = student.user.title
    form.fields['first_name'].initial = student.user.first_name
    form.fields['last_name'].initial = student.user.last_name
    form.fields['username'].initial = student.user.username
    form.fields['email'].initial = student.user.email
    form.fields['contact_number'].initial = student.user.contact_number
    form.fields['student_number'].initial = student.student_number
    form.fields['course_id'].initial = student.course_id.id
    form.fields['session_id'].initial = student.session_id.id
 
    context = {
        "id": student_id,
        "username": student.user.username,
        "form": form
    }
    return render(request, "admin_template/edit_student_template.html", context)

def edit_student_save(request):
    if request.method != "POST":
        return HttpResponse("Invalid Method!")
    else:
        student_id = request.session.get('student_id')
        if student_id == None:
            return redirect('/manage_student')
 
        form = EditStudentForm(request.POST, request.FILES)
        if form.is_valid():
            #title =form.cleaned_data['title']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            contact_number= form.cleaned_data['contact_number']
            student_number = form.cleaned_data['student_number']
            course_id = form.cleaned_data['course_id']
            session_id = form.cleaned_data['session_id']
 
            # Getting Profile Pic first
            # First Check whether the file is selected or not
            # Upload only if file is selected
            if len(request.FILES) != 0:
                profile_pic = request.FILES['profile_pic']
                files = FileSystemStorage()
                filename = files.save(profile_pic.name, profile_pic)
                profile_pic_url = files.url(filename)
            else:
                profile_pic_url = None
 
            try:
                # First Update into Custom User Model
                user = CustomUser.objects.get(id=student_id)
                #user.title = title
                user.first_name = first_name
                user.last_name = last_name
                user.username = username
                user.email = email
                user.contact_number = contact_number
                user.save()
 
                # Then Update Students Table
                student_model = Students.objects.get(user=student_id)
                student_model.student_number = student_number
 
               # module_enrollment= Module_Enrollment.objects.get(id= module_enrollment_id)
                #student_model= module_enrollment_id = module_enrollment
 
                course = Courses.objects.get(id=course_id)
                student_model.course_id = course

                session_obj = Sessions.objects.get(id=session_id)
                student_model.session_id = session_obj

                student_model.student_number = student_number
                if profile_pic_url != None:
                    student_model.profile_pic = profile_pic_url
                student_model.save()
                # Delete student_id SESSION after the data is updated
                del request.session['student_id']
 
                messages.success(request, "Student Updated Successfully!")
                return redirect('/edit_student/'+student_id)
            except:
                messages.success(request, "Failed to Update Student.")
                return redirect('/edit_student/'+student_id)
        else:
            return redirect('/edit_student/'+student_id)

def delete_student(request, student_id):
    student = Students.objects.get(user=student_id)
    try:
        student.delete()
        messages.success(request, "Student Deleted Successfully.")
        return redirect('manage_student')
    except:
        messages.error(request, "Failed to Delete Student.")
        return redirect('manage_student')

def add_module(request):
    courses =Courses.objects.all()
    lecturers = CustomUser.objects.filter(user_role='2')
    context = {
        "courses": courses,
        "lecturers": lecturers
    }
    return render(request, 'admin_template/add_module_template.html', context)

def add_module_save(request):
    if request.method != "POST":
        messages.error(request, "Method Not Allowed!")
        return redirect('add_module')
    else:
        module_name = request.POST.get('module_name')
        module_year =request.POST.get('module_year')


        
 
        course_id = request.POST.get('course')
        course =Courses.objects.get(id=course_id)

        lecturer_id = request.POST.get('lecturer')
        lecturer= CustomUser.objects.get(id=lecturer_id)
 
        try:
            module=Modules(module_name=module_name,
                          module_year = module_year,
                          course_id =course,
                          lecturer_id=lecturer)
            module.save()
            messages.success(request, "Module Added Successfully!")
            return redirect('add_module')
        except:
            messages.error(request, "Failed to Add Module!")
            return redirect('add_module')

def manage_module(request):
    modules = Modules.objects.all()
    context = {
        "modules": modules
    }
    return render(request, 'admin_template/manage_module_template.html', context)


def edit_module(request, module_id):
    module= Modules.objects.get(id=module_id)
    courses =Courses.objects.all()
    lecturers = CustomUser.objects.filter(user_role='2')
    context = {
        "module": module,
        "courses":courses,
        "lecturers": lecturers,
        "id": module_id
    }
    return render(request, 'admin_template/edit_module_template.html', context)

def edit_module_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method.")
    else:
        module_id = request.POST.get('module_id')
        module_name = request.POST.get('module_name')
        module_year =request.POST.get('module_year')

        course_id =request.POST.get('course')
        lecturer_id = request.POST.get('lecturer')
 
        try:
            module = Modules.objects.get(id=module_id)
            module.module_name = module_name
            module.module_year = module_year
            
            course =Courses.objects.get(id =course_id)
            module.course_id= course

            lecturer= CustomUser.objects.get(id=lecturer_id)
            module.lecturer_id = lecturer 
            module.save()
 
            messages.success(request, "Module Updated Successfully.")
             
            return HttpResponseRedirect(reverse("edit_module",
                                                kwargs={"module_id":module_id}))
 
        except:
            messages.error(request, "Failed to Update module.")
            return HttpResponseRedirect(reverse("edit_module",
                                                kwargs={"module_id":module_id}))

def delete_module(request, module_id):
    module= Modules.objects.get(id=module_id)
    try:
        module.delete()
        messages.success(request, "Module Deleted Successfully.")
        return redirect('manage_module')
    except:
        messages.error(request, "Failed to Delete Module.")
        return redirect('manage_module')          
 
@csrf_exempt
def check_email_exist(request):
    email = request.POST.get("email")
    user_obj = CustomUser.objects.filter(email=email).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)
 
 
@csrf_exempt
def check_username_exist(request):
    username = request.POST.get("username")
    user_obj = CustomUser.objects.filter(username=username).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)

#Admin profile
def admin_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
 
    context={
        "user": user
    }
    return render(request, 'admin_template/admin_profile.html', context)
 
def admin_profile_update(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('admin_profile')
    else:
       # title = request.POST.get('title')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
 
        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            #customuser.title =title
            customuser.first_name = first_name
            customuser.last_name = last_name
            if password != None and password != "":
                customuser.set_password(password)
            customuser.save()
            messages.success(request, "Profile Updated Successfully")
            return redirect('admin_profile')
        except:
            messages.error(request, "Failed to Update Profile")
            return redirect('admin_profile')
     
def lecturer_profile(request):
    pass
 
 
def student_profile(requtest):
    pass