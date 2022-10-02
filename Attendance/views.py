import imp
from turtle import title
from django.contrib.auth import login, logout,authenticate
from django.shortcuts import render,HttpResponse,redirect ,HttpResponseRedirect ,reverse
from django.contrib import messages
from django.views.generic import CreateView
from django.contrib.auth.forms import AuthenticationForm
from .models import CustomUser ,Admin,Lecturers,Students
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from .EmailBackends import EmailBackends
from django.contrib.auth import authenticate, login
import json
import requests
from django.contrib.auth.hashers import  make_password
from .Validators import validate_user_mail
#from cryptography.fernet import Fernet




def home(request): 
    return render(request, 'home.html')
 
def loginUser(request):
    return render(request, 'login_page.html')

def doLogin(request):
     
    print("here")
    email = request.GET.get('email')
    password = request.GET.get('password')
    # user_type = request.GET.get('user_type')
    print(email)
    print(password)
    print(request.user)
    if not (email and password):
        messages.error(request, "Please provide all the details!!")
        return render(request, 'login_page.html')
 
    user = CustomUser.objects.filter(email=email, password=password).last()
    if not user:
        messages.error(request, 'Invalid Login Credentials!!')
        return render(request, 'login_page.html')
 
    login(request, user)
    print(request.user)
 
    if user.user_role == CustomUser.STUDENT:
        return redirect('Attendance/student_home/')
    elif user.user_role == CustomUser.LECTURER:
        return redirect('Attendance/lecturer_home/')
    elif user.user_role == CustomUser.ADMIN:
        return redirect('Attendance/admin_home/')
 
    return render(request, 'home.html')


     
def registration(request):
    return render(request, 'registration.html')

 
def doRegistration(request):
    #title = request.GET.get('title')
    first_name = request.GET.get('first_name')
    last_name = request.GET.get('last_name')
    email = request.GET.get('email')
    #email = request.GET.get('email')
    contact_number = request.GET.get('contact_number')
    # password =make_password(request.GET.get('password'))
    # confirm_password =make_password(request.GET.get('confirmPassword'))
    password =request.GET.get('password')
    confirm_password =request.GET.get('confirmPassword')
    #correct_email = validate_user_mail( request.GET.get('email'))

 
    print(email)
    #print(correct_email)
    print(password)
    print(confirm_password)
    print(first_name)
    print(last_name)
    print(contact_number)
    #print(title)

    if not (email and password and confirm_password):
        messages.error(request, 'Please provide all the details!!')
        return render(request, 'registration.html')

    if password != confirm_password:
        messages.error(request, 'Both passwords should match!!')
        return render(request, 'registration.html')
    # if email != correct_email:
    #     messages.error(request, 'Only emails with @ufs.ac.za or @us4life.ac.za are allowed')
    #     return render(request, 'registration.html')
 
    is_user_exists = CustomUser.objects.filter(email=email).exists()
 
    if is_user_exists:
        messages.error(request, 'User with this email  already exists. Please proceed to login!!')
        return render(request, 'registration.html')
 
    user_role = get_user_type_from_email(email)
 
    if user_role is None:
        messages.error(request, "Please use valid format for the email id: '<username>.<lecturer|student|admin>@<atendance_domain>'")
        return render(request, 'registration.html')
 
    username = email.split('@')[0].split('.')[0]
 
    if CustomUser.objects.filter(username=username).exists():
        messages.error(request, 'User with this username already exists. Please use different username')
        return render(request, 'registration.html')
 


 
    user = CustomUser()
    user.username = username
    user.email = email
    user.password = password
    user.user_role = user_role
    user.first_name = first_name
    user.last_name = last_name
    user.contact_number = contact_number
    #user.title = title
    user.save()
     
    if user_role == CustomUser.LECTURER:
        Lecturers.objects.create(user=user)
    elif user_role == CustomUser.STUDENT:
        Students.objects.create(user=user)
    elif user_role== CustomUser.ADMIN:
        Admin.objects.create(user=user)
        
    return render(request, 'login_page.html')
 
     
def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')
 
 
def get_user_type_from_email(email_id):
    """
    Returns CustomUser.user_ROLE corresponding to the given email address
    email_id should be in following format:
    '<username>.<lecturer|student|admin>@<attendance_domain>'
    eg.: 'abhishek.staff@jecrc.com'
    """
 
    try:
        email_id = email_id.split('@')[0]
        email_user_type = email_id.split('.')[1]
        return CustomUser.EMAIL_TO_USER_TYPE_MAP[email_user_type]
    except:
        return None
