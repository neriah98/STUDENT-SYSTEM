from django.db import models
from django.contrib.auth.models import User 
#from students.models import StudentModules
# Create your models here.
class LecturerDeptInfo(models.Model):
    dept_name = models.CharField(max_length=50)

    def __str__(self):
        return self.dept_name

class LecturerSubInfo(models.Model):
    sub_name = models.CharField(max_length=50)

    def __str__(self):
        return self.sub_name

class LecturerInfo(models.Model):
    name = models.OneToOneField(User, on_delete=models.CASCADE ,default=1 )
    full_name = models.CharField(max_length=100 ,null=True,blank=True )
    lecturer_email = models.EmailField(unique=True ,null=True,blank=True)
    lecturer_cellphone = models.CharField(max_length=100 ,null=True,blank=True )
    gender_choice = (
        ("male", "Male"),
        ("Female", "Female"),
    )
    gender = models.CharField(choices=gender_choice, max_length=10) 
    faculty_choice = (
        ("Education", "Education"),
        ("EMS", "EMS"),
         ("Law", "Law"),
          ("Humanities", "Humanities"),
           ("Theology", "Theology"),
            ("NAS", "NAS"),
            ("Health Science", "Health Sciences")
    )
    module = models.ForeignKey("students.StudentModules", on_delete=models.SET_NULL , null=True , related_name="lecturer_modules")
    Faculty = models.CharField( choices=faculty_choice, max_length=100 ,null=True,blank=True )

    def __str__(self):
        return str(self.full_name)
