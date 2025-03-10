from django import forms
from accounts.models import *



class StudentForm(forms.ModelForm):
     class Meta:
          model=Student
          fields = ['student_name','email','img','gender','age','class_id','password']

class FacultyForm(forms.ModelForm):
     class Meta:
          model=Faculty
          fields = ['name','email','image','gender','age','exp','subject','password','is_faculty']

class SubjectForm(forms.ModelForm):
     class Meta:
          model=Subject
          fields = ['subject_name']

class ClassForm(forms.ModelForm):
     class Meta:
          model=Class_Name
          fields = ['class_name','faculty']