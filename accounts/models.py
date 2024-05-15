from django.db import models
from django.contrib.auth.models import User,AbstractUser
# Create your models here.


class Student(models.Model):
    std_id=models.CharField(unique=True,max_length=50)
    first_name=models.CharField(max_length=100,null=True,blank=True)
    last_name=models.CharField(max_length=100,null=True,blank=True)
    email=models.EmailField(null=True,blank=True)
    img=models.FileField(upload_to="student image",null=True,blank=True)
    options=( 
        ("Male","Male"),
        ("Female","Female"),
        ("Others","Others")
    )
    gender=models.CharField(max_length=100,choices=options,default="Male")
    age=models.PositiveIntegerField(null=True)
    d_type=(
        ("Mobility Impairment","Mobility Impairment"), #any full
        ("Visual Impairment","Visual Impairment"),  #audio
        ("Hearing Impairment","Hearing Impairment"), #image
        ("Learning Disability","Learning Disability"), #any
        ("Autism Spectrum Disorder","Autism Spectrum Disorder"), #any
        ("Speech Impairment","Speech Impairment"), #any
        ("Intellectual Disability","Intellectual Disability"), #any
    )
    disability=models.CharField(max_length=100,choices=d_type,default="Mobility Impairment")
    a_techno=(
        ("Screen Reader","Screen Reader"),
        ("Communication App","Communication App"),
        ("Hearing Aids","Hearing Aid"),
        ("Voice Recognition","Voice Recognition"),
        ("Wheelchair","Wheelchair"),
        ("Assistive Learning Tools","Assistive Learning Tools"),
        ("Text-to-Speech Software","Text-to-Speech Software"),
        ("Augmentative and Alternative Communication (AAC) Device","Augmentative and Alternative Communication (AAC) Device"),
    )
    accesstechnology=models.CharField(max_length=200,choices=a_techno,default="Screen Reader")
    # score = models.IntegerField(blank=True,null=True)
    # category = models.CharField(max_length=200,null=True,blank=True)
    # suggestion=models.TextField(null=True,blank=True) 
    # video=models.FileField(upload_to='suggested video',null=True,blank=True)
    # audio=models.FileField(upload_to='suggested audio',null=True,blank=True)

    def __str__(self):
        return self.std_id 
    
class CustUser(AbstractUser):
    student_id=models.ForeignKey(Student,on_delete=models.CASCADE,related_name='cust',null=True)
    

    
class Types(models.Model):
    names=models.CharField(max_length=100)    

    def __str__(self):
        return self.names

class Question(models.Model):
    text = models.TextField(null=True,blank=True)
    type=models.ForeignKey(Types,on_delete=models.CASCADE,null=True,default=1)
    
    def __str__(self):
        return self.text

class QuestionImages(models.Model):
    files=models.FileField(upload_to='media/files_queimg',null=True,blank=True)
    type=models.ForeignKey(Types,on_delete=models.CASCADE,null=True,default=3)

    def __str__(self):
       return f" {self.files.name}" if self.type else f"Unknown Type - {self.files.name}"

class QuestionAudio(models.Model):
    files=models.FileField(upload_to='media/files_queaudio',null=True,blank=True)
    type=models.ForeignKey(Types,on_delete=models.CASCADE,null=True,default=2)

    def __str__(self):
       return f" {self.files.name}" if self.type else f"Unknown Type - {self.files.name}"

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=255,null=True,blank=True)
    is_correct = models.BooleanField(default=False)
    
class AnswerImages(models.Model):
    question = models.ForeignKey(QuestionImages, on_delete=models.CASCADE)
    fileans=models.FileField(upload_to='media/files_queimageans',null=True,blank=True)
    is_correct = models.BooleanField(default=False)
    
class AnswerAudio(models.Model):
    question = models.ForeignKey(QuestionAudio, on_delete=models.CASCADE)
    fileans=models.FileField(upload_to='media/files_queaudioans',null=True,blank=True)
    is_correct = models.BooleanField(default=False)
    
   
   
    
class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name     
    
class Categorys(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name     

class StudentAnswer(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE,null=True)

   

class StudentAnswerImage(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    question = models.ForeignKey(QuestionImages, on_delete=models.CASCADE)
    answer = models.ForeignKey(AnswerImages, on_delete=models.CASCADE,null=True)


class StudentAnswerAudio(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    question = models.ForeignKey(QuestionAudio, on_delete=models.CASCADE)
    answer = models.ForeignKey(AnswerAudio, on_delete=models.CASCADE,null=True)

    

class ScoreModel(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    score = models.IntegerField(blank=True,null=True)
    cat = models.ForeignKey(Categorys,on_delete=models.CASCADE,null=True,blank=True)
    suggestion=models.TextField(null=True,blank=True) 
    video=models.FileField(upload_to='suggested video',null=True,blank=True)
    audio=models.FileField(upload_to='suggested audio',null=True,blank=True)
  
    
class Suggestion(models.Model):
     suggestion=models.TextField(null=True)  
     cat=models.ForeignKey(Categorys,on_delete=models.CASCADE,related_name='sugg')  
     video=models.FileField(upload_to='suggested video',null=True)
     audio=models.FileField(upload_to='suggested audio',null=True)
     thumbnail = models.ImageField(upload_to='thumbnails/', blank=True, null=True)
     
     def __str__(self):
        return self.cat.name
     
# class Assignment(models.Model): 
#     student=models.ForeignKey(Student,on_delete=models.CASCADE,related_name='stu_ag')
#     test=models.ForeignKey(Question,on_delete=models.CASCADE,related_name='tes_ag')     




 


