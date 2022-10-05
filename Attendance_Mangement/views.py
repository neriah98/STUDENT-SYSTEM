from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from students.models import *
from lecturers.models import *

@login_required
def index(request):
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
            
            
        context = {"students":students, "logged_in_as_student":logged_in_as_student,"logged_in_as_lecturer":logged_in_as_lecturer,"lecturers":lecturers}
        return render(request, "home.html", context)
    
    
    else:
        logged_in_as_student = ""
        logged_in_as_lecturer = ""
        context = {"students":students, "logged_in_as_lecturer":logged_in_as_student,"logged_in_as_lecturer":logged_in_as_lecturer,"teachers":lecturers}
        return render(request, "home.html", context)



