#from django.contrib import admin
from django.urls import path, include

from Attendance import StudentViews
from . import views
from .import AdminViews
from .import LecturerViews



urlpatterns = [
    #path('admin/', admin.site.urls),
    path('', views.home, name="home"),
    path('login', views.loginUser, name="login"),
    path('logout_user', views.logout_user, name="logout_user"),
    path('registration', views.registration, name="registration"),
    path('doLogin', views.doLogin, name="doLogin"),
    path('doRegistration', views.doRegistration, name="doRegistration"),


       #URLS admin views/courses
    path('add_course/', AdminViews.add_course, name="add_course"),
    path('add_course_save/', AdminViews.add_course_save, name="add_course_save"),
    path('manage_course/', AdminViews.manage_course, name="manage_course"),
    path('edit_course/<course_id>/', AdminViews.edit_course, name="edit_course"),
    path('edit_course_save/', AdminViews.edit_course_save, name="edit_course_save"),
    path('delete_course/<course_id>/', AdminViews.delete_course, name="delete_course"),



    #URLS FOR ADMIN
    path('admin_home/', AdminViews.admin_home, name="admin_home"),
    #admin/lecturers views
    path('add_lecturer/', AdminViews.add_lecturer, name="add_lecturer"),
    path('add_lecturer_save/', AdminViews.add_lecturer_save, name="add_lecturer_save"),
    path('manage_lecturer/', AdminViews.manage_lecturer, name="manage_lecturer"),
    path('edit_lecturer/<lecturer_id>/', AdminViews.edit_lecturer, name="edit_lecturer"),
    path('edit_lecturer_save/', AdminViews.edit_lecturer_save, name="edit_lecturer_save"),
    path('delete_lecturer/<lecturer_id>/', AdminViews.delete_lecturer, name="delete_lecturer"),
      #admin/module views
    path('add_module/', AdminViews.add_module, name="add_module"),
    path('add_module_save/', AdminViews.add_module_save, name="add_module_save"),
    path('manage_module/', AdminViews.manage_module, name="manage_module"),
    path('edit_module/<module_id>/', AdminViews.edit_module, name="edit_module"),
    path('edit_module_save/', AdminViews.edit_module_save, name="edit_module_save"),
    path('delete_module/<module_id>/', AdminViews.delete_module, name="delete_module"),

     #admin/venue urls
    # path('add_venue/', AdminViews.add_venue, name="add_venue"),
    # path('add_venue_save/', AdminViews.add_venue_save, name="add_venue_save"),
    # path('manage_venue/', AdminViews.manage_venue, name="manage_venue"),
    # path('edit_venue/<venue_id>/', AdminViews.edit_venue, name="edit_venue"),
    # path('edit_venue_save/', AdminViews.edit_venue_save, name="edit_venue_save"),
    # path('delete_venue/<venue_id>/', AdminViews.delete_venue, name="delete_venue"),




     
     #admin/session views
    path('manage_session/', AdminViews.manage_session, name="manage_session"),
    path('add_session/', AdminViews.add_session, name="add_session"),
    path('add_session_save/', AdminViews.add_session_save, name="add_session_save"),
    path('edit_session/<session_id>', AdminViews.edit_session, name="edit_session"),
    path('edit_session_save/', AdminViews.edit_session_save, name="edit_session_save"),
    path('delete_session/<session_id>/', AdminViews.delete_session, name="delete_session"),


    #admin/student views

    path('add_student/', AdminViews.add_student, name="add_student"),
    path('add_student_save/', AdminViews.add_student_save, name="add_student_save"),
    path('edit_student/<student_id>', AdminViews.edit_student, name="edit_student"),
    path('edit_student_save/', AdminViews.edit_student_save, name="edit_student_save"),
    path('manage_student/', AdminViews.manage_student, name="manage_student"),
    path('delete_student/<student_id>/', AdminViews.delete_student, name="delete_student"),

    #admin views/check username and email views
    path('check_email_exist/', AdminViews.check_email_exist, name="check_email_exist"),
    path('check_username_exist/', AdminViews.check_username_exist, name="check_username_exist"),

      #admin.dmin views profile
    path('admin_profile/', AdminViews.admin_profile, name="admin_profile"),
    path('admin_profile_update/', AdminViews.admin_profile_update, name="admin_profile_update"),


    #URLS FOR LECTURER
      path('lecturer_home/', LecturerViews.lecturer_home, name="lecturer_home"),


    #Paths for Student
     path('student_home/', StudentViews.student_home, name="student_home"),
]