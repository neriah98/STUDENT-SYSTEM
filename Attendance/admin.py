from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser,Lecturers ,Admin, Sessions,Students,Attendance,Modules,Courses,Sessions ,Venues

# Register your models here.
# class UserModel(UserAdmin):
#     ordering = ('email',)

admin.site.register(CustomUser)
admin.site.register(Lecturers)
admin.site.register(Admin)
admin.site.register(Students)
admin.site.register(Sessions)
admin.site.register(Venues)
admin.site.register(Modules)
admin.site.register(Courses)
admin.site.register(Attendance)