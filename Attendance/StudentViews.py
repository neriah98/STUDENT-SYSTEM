from django.shortcuts import render, redirect



def student_home(request):
    return render(request, "student_template/student_home.html")