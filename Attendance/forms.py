from django import forms
from .models import Courses, Sessions


# class DateInput(forms.DateInput):
#     input_type = "date"


class AddStudentForm(forms.Form):
    # title_list = (
    #     ('MR','MR'),
    #     ('MRS','MRS'),
    #     ('MISS','MISS'),
    #     ('PROF','PROF'),
    #     ('DR','DR'),
    # )
    # title = forms.ChoiceField(label="Title", choices=title_list, widget=forms.Select(attrs={"class":"form-control"}))
    first_name = forms.CharField(label="First Name", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name = forms.CharField(label="Last Name", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    username = forms.CharField(label="Username", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    email = forms.EmailField(label="Email", max_length=50, widget=forms.EmailInput(attrs={"class":"form-control"}))
    contact_number= forms.CharField(label="Contact Number", max_length=15, widget=forms.TextInput(attrs={"class":"form-control"}))
    student_number= forms.CharField(label="Student Number", max_length=10, widget=forms.TextInput(attrs={"class":"form-control"}))
    password = forms.CharField(label="Password", max_length=50, widget=forms.PasswordInput(attrs={"class":"form-control"}))
    
    
    


    #For Displaying Courses
    try:
        courses = Courses.objects.all()
        course_list = []
        for course in courses:
            single_course = (course.id, course.course_name)
            course_list.append(single_course)
    except:
        print("here")
        course_list = []
    
    #For Displaying Sessions
    try:
        sessions =Sessions.objects.all()
        session_list = []
        for session in sessions:
            single_session = (session.id,session.session_name , str(session.session_date)+" to "+str(session.session_time))
            session_list.append(single_session)
            
    except:
        session_list = []
    
    
 
    
    course_id = forms.ChoiceField(label="Course", choices=course_list, widget=forms.Select(attrs={"class":"form-control"}))
    session_id = forms.ChoiceField(label="Session ", choices=session_list, widget=forms.Select(attrs={"class":"form-control"}))
    profile_pic = forms.FileField(label="Profile Pic", required=False, widget=forms.FileInput(attrs={"class":"form-control"}))



class EditStudentForm(forms.Form):
    # title_list = (
    #     ('MR','MR'),
    #     ('MRS','MRS'),
    #     ('MISS','MISS'),
    #     ('PROF','PROF'),
    #     ('DR','DR'),
    # )



    # title = forms.ChoiceField(label="Title", choices=title_list, widget=forms.Select(attrs={"class":"form-control"}))
    first_name = forms.CharField(label="First Name", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name = forms.CharField(label="Last Name", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    username = forms.CharField(label="Username", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    email = forms.EmailField(label="Email", max_length=50, widget=forms.EmailInput(attrs={"class":"form-control"}))
    contact_number= forms.CharField(label="Contact Number", max_length=15, widget=forms.TextInput(attrs={"class":"form-control"}))
    student_number= forms.CharField(label="Student Number", max_length=10, widget=forms.TextInput(attrs={"class":"form-control"}))
   
    
  #For Displaying Courses
    try:
        courses = Courses.objects.all()
        course_list = []
        for course in courses:
            single_course = (course.id, course.course_name)
            course_list.append(single_course)
    except:
        print("here")
        course_list = []
    
    #For Displaying Sessions
    try:
        sessions = Sessions.objects.all()
        session_list = []
        for session in sessions:
            single_session = (session.id,session.session_name , str(session.session_date)+" to "+str(session.session_time))
            session_list.append(single_session)
            
    except:
        session_list = []

    

    
    course_id = forms.ChoiceField(label="Course", choices=course_list, widget=forms.Select(attrs={"class":"form-control"}))
    session_id = forms.ChoiceField(label="Session ", choices=session_list, widget=forms.Select(attrs={"class":"form-control"}))
    profile_pic = forms.FileField(label="Profile Pic", required=False, widget=forms.FileInput(attrs={"class":"form-control"}))