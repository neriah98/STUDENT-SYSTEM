from email.policy import default
from pyexpat import model
from statistics import mode
from unittest.util import _MAX_LENGTH
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from Attendance.models import *
from PIL import Image
from django.contrib.auth.models import UserManager
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from .Validators import validate_user_mail


#Managers
class CustomUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = CustomUser(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        assert extra_fields["is_staff"]
        assert extra_fields["is_superuser"]
        return self._create_user(email, password, **extra_fields)



# CREATE USER MODELS HERE(TABLES IN YOUR DATABASE)

#This is the User table
class CustomUser(AbstractUser):
    ADMIN ='1'
    LECTURER ='2'
    STUDENT = '3'
    #SUPER_ADMIN = '4'

    EMAIL_TO_USER_TYPE_MAP = {
        'admin': ADMIN,
        'lecturer': LECTURER,
        'student': STUDENT,
        #'super_admin':SUPER_ADMIN,
    }

    # TITLE = (
    #     ('MR','MR'),
    #     ('MRS','MRS'),
    #     ('MISS','MISS'),
    #     ('PROF','PROF'),
    #     ('DR','DR'),
    # )

    #Create an email validator function

    # def validate_user_mail(value):
    #     if "@ufs.ac.za" or "@ufs4life.ac.za" in value:
    #         return value
    #     else:
    #         raise ValidationError("Only emails with @ufs.ac.za and @ufs4life.ac.za are allowed")


         #Fields
    # title= models.CharField(max_length=5, null=True, choices=TITLE)
    email = models.EmailField(_('email address'),unique =True)
       #validators=[validate_user_mail]
     
    contact_number = models.CharField(max_length=15)
    user_role_data = ((ADMIN, "ADMIN"), (LECTURER, "Lecturer"), (STUDENT, "Student") )
    user_role= models.CharField(default=1, choices=user_role_data, max_length=15)
    #profile_pic = models.ImageField(upload_to ="images/")
 

    USERNAME_FIELD ='email'
    REQUIRED_FIELDS =[]

    # objects = CustomUserManager()
    objects = CustomUserManager()


    def __str__(self):
        return self.first_name + " " + self.last_name  + " "  + self.email




class Lecturers(models.Model):
     id = models.AutoField(primary_key=True)
     user= models.OneToOneField(CustomUser, on_delete = models.CASCADE)
     office_number = models.CharField(max_length=255)
     objects = CustomUserManager()
    
     def __str__(self):
        return self.user.last_name + " ," + self.user.first_name


class Courses(models.Model):
  
    id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = CustomUserManager()


class Modules(models.Model):

    # MODULES = (
    #     ('BCIS1513','BCIS1513'),
    #     ('CSIS2614','CSIS2614'),
    #     ('CSIS2664','CSIS2664'),
    #     ('CSIS3744','CSIS3744'),
    #     ('CSIS3734','CSIS3734'),
    #     ('CSIA6843','CSIA6843'),
    #     ('CSIS3714','CSIS3714'),
    # )


    # MODULES_DESCRIPTION = (
    #     ('INTRO TO INFORMATION SYSTEMS','INTRO TO INFORMATION SYSTEMS'),
    #     ('DATA STRUCTURES','DATA STRUCTURES'),
    #     ('SOFTWARE DESIGN','SOFTWARE DESIGN'),
    #     ('COMPUTER NETWORKS','COMPUTER NETWORKS'),
    #     ('INTERNET PROGRAMMING','INTERNET PROGRAMMING'),
    #     ('ANALYTICAL PROGRAMMING','ANALYTICAL PROGRAMMING'),
    #     ('INTRO TO DATABASES','INTRO TO DATABASES'),

    # )


    # MODULES_CAMPUS =(
    #     ('BFN','BFN'),
    #     ('QWAQWA','QWAQWA'),

    # )

    # MODULES_YEAR =(
    #     ('1','1'),
    #     ('2','2'),
    #     ('3','3'),
    #     ('4','4'),
    # )

    id = models.AutoField(primary_key=True)
    module_name = models.CharField(max_length=255)
    module_year = models.CharField(max_length=30 )
    course_id = models.ForeignKey(Courses , on_delete=models.CASCADE ,default=1)
    lecturer_id = models.ForeignKey(Lecturers,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = CustomUserManager()
  

    def __str__(self):
        return self.module_name


class Admin(models.Model):
     id = models.AutoField(primary_key=True)
     user= models.OneToOneField(CustomUser, on_delete = models.CASCADE)
     created_at = models.DateTimeField(auto_now_add=True)
     updated_at = models.DateTimeField(auto_now=True)
     objects = CustomUserManager()


class Venues(models.Model):
    id = models.AutoField(primary_key=True)
    venue_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = CustomUserManager()

    def __str__(self):
        return self.venue_name



class Sessions(models.Model):

    id = models.AutoField(primary_key=True)
    session_name = models.CharField(max_length=100)
    session_date= models.DateField()
    session_time = models.TimeField()
    #venue_id = models.ForeignKey(Venues , on_delete=models.CASCADE ,default=1)
    #session_is_active = models.BooleanField(default=False)
    # module_id = models.ForeignKey(Module, on_delete=models.CASCADE)
    # venue_id= models.ForeignKey(Venue, on_delete=models.CASCADE)
    objects = CustomUserManager()
    

    def __str__(self):
        return self.session_name + "" + self.session_date + " " + self.session_time
     


#Directory to store student images
def student_directory_path(instance, filename): 
    name, ext = filename.split(".")
    name = instance.student_number + "_" + instance.student_number + "_" + instance.course_id
    filename = name +'.'+ ext 
    return 'Student_Images/{}/{}/{}/{}'.format(instance.student_number,instance.course_id,filename)





class Students(models.Model):
     id = models.AutoField(primary_key=True)
     user= models.OneToOneField(CustomUser, on_delete = models.CASCADE)
     student_number = models.CharField(max_length=10)
     profile_pic =models.ImageField(upload_to=student_directory_path ,null=True, blank=True)
     course_id = models.ForeignKey(Courses ,on_delete=models.DO_NOTHING , default=1)
     session_id = models.ForeignKey(Sessions, null=True,on_delete=models.CASCADE)
     
     created_at = models.DateTimeField(auto_now_add=True)
     updated_at = models.DateTimeField(auto_now=True)
     objects = CustomUserManager() 

     def __str__(self):
        return self.user.last_name + " ," + self.user.first_name

#OTHER MODELS RELATED TO ATTENDANCE



     



class Attendance(models.Model):
    id = models.AutoField(primary_key=True)
    attendance_date= models.DateField()
    attendance_time = models.TimeField()
    student_id = models.ForeignKey(Students,on_delete=models.DO_NOTHING)
    module_id = models.ForeignKey(Modules ,on_delete=models.DO_NOTHING)
    session_id= models.ForeignKey(Sessions, on_delete=models.CASCADE)
    status = models.CharField(max_length=200, null = True, default='Absent')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = CustomUserManager()

    def __str__(self):
        return str(self.student_id+ "_" + str(self.attendance_date)+ "_" + str(self.attendance_time + "_" +str(self.module_id)))




#Creating Django Signals

@receiver(post_save, sender=CustomUser)
# Now Creating a Function which will
# automatically insert data in Admin, lecturer or Student
def create_user_profile(sender, instance, created, **kwargs):
    # if Created is true (Means Data Inserted)
    if created:
        if instance.user_role == 1:
            Admin.objects.create(user=instance)
        if instance.user_role == 2:
            Lecturers.objects.create(user=instance)
        if instance.user_role == 3:
            Students.objects.create(user=instance)
     
 
@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_role == 1:
        instance.admin.save()
    if instance.user_role == 2:
        instance.lecturers.save()
    if instance.user_role == 3:
        instance.students.save()


