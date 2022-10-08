from django.shortcuts import render, redirect
from django.contrib.auth.models import User 
from .models import *
from .forms import SignUpForm
from django.contrib.auth import login
# Create your views here.

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
            adminProfiles = AdminInfo.objects.create( name = users , admin_email=users.email,full_name=users.get_full_name())
            adminProfiles.save()

            new_user.save()
           #if user is active ,then they can login ,if not redirect to waiting page
            login(request, new_user)
            return redirect('home')
    context = {'form': form}
    return render(request, 'admins/registration/register.html', context)

