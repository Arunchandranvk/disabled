from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import TemplateView,CreateView
from accounts.models import *
from django.urls import reverse_lazy
from .forms import *
from django.http import HttpResponse
# Create your views here.

# @receiver(post_save, sender=Student)
# def create_user_from_student(sender, instance, created, **kwargs):
#     if created:
#         CustUser= get_user_model()
#         email = instance.e
#         password = 'admin@123' 
#         CustUser.objects.create_user(email=email, password=password,student_id_id=student_id_id)


class AdminHome(TemplateView):
    template_name='admin_home.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['faculty'] = Faculty.objects.all()[:4]
        context['students'] = Student.objects.all()[:4]
        return context

class FacultyList(TemplateView):
    template_name='faculty_list.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['faculty'] = Faculty.objects.all()
        return context

class StudentsList(TemplateView):
    template_name='students_list.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['students'] = Student.objects.all()
        return context
    

class AddStudent(CreateView):
    template_name='addstudent.html'
    model=Student 
    form_class=StudentForm 
    success_url=reverse_lazy('students')
    def get_context_data(self, **kwargs):
        context =super().get_context_data(**kwargs)  
        context['class']=Class_Name.objects.all()
        return context
    

class AddFaculty(CreateView):
    template_name='addfaculty.html'
    model=Faculty 
    form_class=FacultyForm
    success_url=reverse_lazy('faculty')
    def get_context_data(self, **kwargs):
        context =super().get_context_data(**kwargs)  
        context['subject']=Subject.objects.all()
        return context
    

    
class AddSubject(CreateView):
    template_name='subjects.html'
    model=Subject 
    form_class=SubjectForm
    success_url=reverse_lazy('add-sub')
    def get_context_data(self, **kwargs):
        context =super().get_context_data(**kwargs)  
        context['subject']=Subject.objects.all()
        return context

class AddClass(CreateView):
    template_name='class.html'
    model=Class_Name 
    form_class=ClassForm
    success_url=reverse_lazy('add-cls')
    def get_context_data(self, **kwargs):
        context =super().get_context_data(**kwargs)  
        context['class']=Class_Name.objects.all()
        context['faculty']=Faculty.objects.all()
        return context
    

def remove_faculty(req,pk):
    try:
        faculty= get_object_or_404(CustUser,id=pk)
        faculty.delete()
        faculty.save()
        return redirect('faculty')
    except Exception as e:
        return HttpResponse(f"An error occurred: {str(e)}", status=500)
    

def remove_student(req,pk):
    try:
        stu= get_object_or_404(CustUser,id=pk)
        stu.delete()
        stu.save()
        return redirect('students')
    except Exception as e:
        return HttpResponse(f"An error occurred: {str(e)}", status=500)
    
def remove_class(req,pk):
    try:
        cls= Class_Name.objects.get(id=pk)
        print(cls.class_name)
        print(cls.id)
        cls.delete()
        # cls.save()
        return redirect('add-cls')
    except Exception as e:
        return HttpResponse(f"An error occurred: {str(e)}", status=500)
    
def remove_subject(req,pk):
    try:
        sub= get_object_or_404(Subject,id=pk)
        sub.delete()
        # sub.save()
        return redirect('add-sub')
    except Exception as e:
        return HttpResponse(f"An error occurred: {str(e)}", status=500)
