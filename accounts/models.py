from django.db import models
from django.contrib.auth.models import User,AbstractUser
import os
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.db.models import Max
from django.contrib.auth.hashers import make_password


def user_directory_path(instance, filename):
    """
    This function renames the uploaded image file to the username of the user.
    """
    extension = filename.split('.')[-1]  
    new_filename = f"{instance.std_id}.{extension}"  
    return os.path.join('student image', new_filename) 


class CustomUserManager(BaseUserManager):
    def create_user(self, email,password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email ,**extra_fields)
        if password:
            # try:
            #     validate_password(password, user)
            # except ValidationError as e:
            #     raise ValueError(f"Password validation error: {e.messages}")
            user.set_password(password)
        else:
            raise ValueError("Password is required")
        user.save(using=self._db)
        return user

    def create_superuser(self, email,password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email,password, **extra_fields)


class CustUser(AbstractBaseUser,PermissionsMixin):
    email=models.EmailField(unique=True)
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_faculty=models.BooleanField(default=False)
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['email']

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser
    
    def __str__(self):
        return self.email

class Subject(models.Model):
    subject_name=models.CharField(max_length=100)

    def __str__(self):
        return self.subject_name

class Faculty(CustUser):
    name=models.CharField(max_length=100)
    options=( 
        ("Male","Male"),
        ("Female","Female"),
        ("Others","Others")
    )
    gender=models.CharField(max_length=100,choices=options,default="Male")
    age=models.IntegerField() 
    exp=models.IntegerField(default=1) 
    image=models.ImageField(upload_to="Faculty Image",null=True)
    subject=models.ForeignKey(Subject,on_delete=models.CASCADE)
    def save(self, *args, **kwargs):
        if self.pk is None or not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Class_Name(models.Model):
    class_name=models.CharField(unique=True,max_length=100)
    faculty=models.OneToOneField(Faculty,on_delete=models.CASCADE,related_name='fac_class')

    def __str__(self):
        return self.class_name

class Student(CustUser):
    std_id=models.CharField(unique=True,max_length=50)
    student_name=models.CharField(max_length=100,null=True,blank=True)
    img=models.FileField(upload_to=user_directory_path,null=True,blank=True)
    options=( 
        ("Male","Male"),
        ("Female","Female"),
        ("Others","Others")
    )
    gender=models.CharField(max_length=100,choices=options,default="Male")
    age=models.PositiveIntegerField(null=True)
    class_id=models.ForeignKey(Class_Name,on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.std_id:  
            last_std_id = Student.objects.aggregate(max_id=Max('std_id'))['max_id']
            if last_std_id:
                new_id = int(last_std_id[3:]) + 1
            else:
                new_id = 1
            self.std_id = f"STU{new_id:04d}"  
        if self.pk is None or not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        
        super().save(*args, **kwargs)

    def __str__(self):
        return self.std_id 
    

class  Exam(models.Model):
    faculty=models.ForeignKey(Faculty,on_delete=models.CASCADE,related_name='fac_exams')
    exam_name=models.CharField(max_length=100)
    is_active=models.BooleanField(default=False)
    total_score = models.IntegerField(default=50)
    duration=models.IntegerField(default=5)
    date=models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return self.exam_name
    
class ExamQuestions(models.Model):
    exam=models.ForeignKey(Exam,on_delete=models.CASCADE)
    question=models.TextField()
    option_1=models.CharField(max_length=200)
    option_2=models.CharField(max_length=200)
    option_3=models.CharField(max_length=200)
    option_4=models.CharField(max_length=200)
    answer=models.CharField(max_length=200)
    created_at=models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return self.question


class AssignExam(models.Model):
    faculty=models.ForeignKey(Faculty,on_delete=models.CASCADE,related_name='assign_class')
    exam=models.ForeignKey(Exam,on_delete=models.CASCADE)
    class_id=models.ForeignKey(Class_Name,on_delete=models.CASCADE)
    

    def __str__(self):
        return self.exam.exam_name


class ExamResult(models.Model):
    assignedexam=models.ForeignKey(AssignExam,on_delete=models.CASCADE)
    student=models.ForeignKey(Student,on_delete=models.CASCADE)
    question=models.ForeignKey(ExamQuestions,on_delete=models.CASCADE,related_name='exam_ques')
    ans=models.CharField(max_length=200,null=True,blank=True)
    is_correct=models.BooleanField(null=True,blank=True,default=False)

    def __str__(self):
        return f"{self.student.student_name} - {self.assignedexam.exam.exam_name}"
   
    
class Categorys(models.Model):
    name = models.CharField(max_length=255)
    suggestion = models.TextField(null=True)

    def __str__(self):
        return self.name     


class ScoreModel(models.Model):
    assignedexam=models.ForeignKey(AssignExam,on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE,related_name='score_student')
    score = models.IntegerField(blank=True,null=True)
    cat = models.ForeignKey(Categorys,on_delete=models.CASCADE,null=True,blank=True)



    
class HistoryExam(models.Model):
    assignedexam=models.ForeignKey(AssignExam,on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE,related_name='score_student_history')
    score = models.IntegerField(blank=True,null=True)
    cat = models.ForeignKey(Categorys,on_delete=models.CASCADE,null=True,blank=True)

        




 


