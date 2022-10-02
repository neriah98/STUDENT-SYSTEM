from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage #To upload Profile Picture
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import CustomUser ,Modules,Lecturers

def lecturer_home(request):
    return render(request, "lecturer_template/lecturer_home.html")