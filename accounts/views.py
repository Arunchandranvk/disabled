from typing import Any
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render,redirect,HttpResponseRedirect
from .models import *
from .models import Question
from .forms import *
from django.views.generic import FormView,CreateView,UpdateView,TemplateView,View
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse_lazy
from django.contrib.auth.hashers import make_password
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from .models import Suggestion
from student_app.forms import ChangePasswordForm
from django.forms import formset_factory
# Create your views here.

import pandas as pd
import random
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.http import JsonResponse

from django.contrib.auth import logout as auth_logout

def custom_logout(request):
    # Add any custom logout logic here
    auth_logout(request)
    return redirect('log')

class MainHome(TemplateView):
    template_name="mainhome.html"

class ClearDataView(View):
    def post(self, request):
        StudentAnswer.objects.all().delete()
        StudentAnswerImage.objects.all().delete()
        StudentAnswerAudio.objects.all().delete()
        ScoreModel.objects.all().delete()
        return JsonResponse({'message': 'Data cleared successfully'})

@receiver(post_save, sender=Student)
def create_user_from_student(sender, instance, created, **kwargs):
    if created:
        # User = get_user_model()
        CustUser= get_user_model()
        student_id_id=instance.id
        username = instance.std_id
        password = 'admin@123'  # Set your desired default password here
        # User.objects.create_user(username=username, password=password)
        CustUser.objects.create_user(username=username, password=password,student_id_id=student_id_id)
        # ScoreModel.objects.create(student_id=student_id_id)

class LoginView(FormView):
    template_name="login.html"
    form_class=LogForm
    def post(self,request,*args,**kwargs):
        log_form=LogForm(data=request.POST)
        if log_form.is_valid():  
            us=log_form.cleaned_data.get('username')
            ps=log_form.cleaned_data.get('password')
            user=authenticate(request,username=us,password=ps)
            if user: 
                login(request,user)
                if request.user.is_superuser == 1:
                    return redirect('h')
                else:
                    return redirect('sh')
            else:
                return render(request,'login.html',{"form":log_form})
        else:
            return render(request,'login.html',{"form":log_form})  

    

class AddStudent(CreateView):
    template_name='addstudent.html'
    model=Student
    form_class=StudentForm 
    success_url=reverse_lazy('stu')  
    



class QuestView(TemplateView):
    template_name='test.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id=kwargs.get('pk')
        context['stu']=Student.objects.get(id=id)
        context['ques']=Question.objects.all()      
        return context

    
# class QuestViewAll(TemplateView):
#     template_name='Assignexam.html'
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['stu']=Student.objects.all()
#         context['ques'] = Question.objects.all()
#         return context    
    
# class QuestViewImageAll(TemplateView):
#     template_name='testallimage.html'
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['stu']=Student.objects.all()
#         context['ques'] = QuestionImages.objects.all()
#         return context    
    
# class QuestViewAudioAll(TemplateView):
#     template_name='testallaudio.html'
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['stu']=Student.objects.all()
#         context['ques'] = QuestionAudio.objects.all()
#         return context    

def Test(request,**kwargs):
    if request.method == 'POST':
        id=kwargs.get('pk')
        stu=Student.objects.get(id=id)
        que=Question.objects.all()
        assignment = StudentAnswer(student=stu, question=que)
        assignment.save()
        return redirect('det')    

from django.core.mail import send_mail

def AssignView(request,**kwargs):
    if request.method == 'POST':
        # Get all available tests
        tests = Question.objects.all()

        # Get all students
        students = Student.objects.filter(disability__in=["Mobility Impairment", "Learning Disability", "Autism Spectrum Disorder", "Speech Impairment", "Intellectual Disability","Hearing Impairment"])
        students_with_email_sent = set()
        # Assign all tests to all students
        for test in tests:
            for student in students:
                
                assignment, created = StudentAnswer.objects.get_or_create(student=student, question=test)
                if created:
                    assignment.save()
                    subject = 'Test Assignment'
                    message = f'You have been assigned the test. Check your dashboard for details.'
                    from_email = 'testhelloability@gmail.com' 
                    
                    to_email = [student.email]
                    if student in students_with_email_sent:
                                continue
                    send_mail(subject, message, from_email, to_email, fail_silently=False)
                    students_with_email_sent.add(student)

        return redirect('testall') 

    # Retrieve all available tests
    tests = Question.objects.all()

    return render(request, 'Assignexam.html', {'tests': tests})          


def AssignImageView(request,**kwargs):
    if request.method == 'POST':
        # Get all available tests

        tests = QuestionImages.objects.all()

        # Get all students
        students = Student.objects.filter(disability="Hearing Impairment")
        students_with_email_sent = set()
        # Assign all tests to all students
        for test in tests:
            for student in students:
                
                assignment, created = StudentAnswerImage.objects.get_or_create(student=student, question=test)
                if created:
                    assignment.save()
                    subject = 'Test Assignment'
                    message = f'You have been assigned the test. Check your dashboard for details.'
                    from_email = 'testhelloability@gmail.com' 
                    to_email = [student.email]
                    if student in students_with_email_sent:
                        continue
                    send_mail(subject, message, from_email, to_email, fail_silently=False)
                    students_with_email_sent.add(student)

        return redirect('testallvisual') 

    # Retrieve all available tests
    tests = QuestionImages.objects.all()

    return render(request, 'testallimage.html', {'tests': tests})          


def AssignAudioView(request,**kwargs):
    if request.method == 'POST':
        # Get all available tests
        tests = QuestionAudio.objects.all()

        # Get all students
        students = Student.objects.filter(disability="Visual Impairment")
        students_with_email_sent = set()

        # Assign all tests to all students
        for test in tests:
            for student in students:
                

                assignment, created = StudentAnswerAudio.objects.get_or_create(student=student, question=test)
                
                if created:
                    assignment.save()
                    
                    subject = 'Test Assignment'
                    message = 'You have been assigned the test. Check your dashboard for details.'
                    from_email = 'donkannukkadan@gmail.com'
                    to_email = [student.email]
                    if student in students_with_email_sent:
                        continue
                    # Send email
                    send_mail(subject, message, from_email, to_email, fail_silently=False)

                    # Add the student to the set of students with sent emails
                    students_with_email_sent.add(student)

        return redirect('testallhear') 

    # Retrieve all available tests
    tests = QuestionAudio.objects.all()

    return render(request, 'testallaudio.html', {'tests': tests})          
 


from random import sample

class Quesadd(CreateView):
    template_name="quesadd.html"
    model=Question
    form_class=QuesForm
    success_url=reverse_lazy('qans')
    def get_context_data(self, **kwargs) :
        context = super().get_context_data(**kwargs) 
        context['tests'] = Question.objects.all()
        return context

class Quesimage(CreateView):
    template_name="quesimage.html"
    model=QuestionImages
    form_class=QuesFormImage
    success_url=reverse_lazy('qansimg')
    def get_context_data(self, **kwargs) :
        context = super().get_context_data(**kwargs) 
        context['tests'] = QuestionImages.objects.all()
        return context
    
class Quesaudio(CreateView):
    template_name="quesaudio.html"
    model=QuestionAudio
    form_class=QuesFormAudio
    success_url=reverse_lazy('qansaudio')
    def get_context_data(self, **kwargs) :
        context = super().get_context_data(**kwargs) 
        context['tests'] = QuestionAudio.objects.all()
        return context

class QuesUpdate(UpdateView):
    template_name="questionupdate.html"
    model=Question
    form_class=QuesForm
    success_url=reverse_lazy('qdel') 
    def get_context_data(self, **kwargs) :
        context = super().get_context_data(**kwargs)
        context['tests']=Question.objects.all()
        return context     
 
class QuesAnsUpdView(CreateView):
    template_name="quesansupdate.html"
    model=Answer
    form_class=QuesAnsForm
    success_url=reverse_lazy('qdel') 
    def form_valid(self, form):
        # Save the main answer
        main_answer = form.save(commit=False)
        main_answer.save()

        # Get additional options from the form data
        option_texts = [self.request.POST.get(f'option_{i}') for i in range(1, 4)]

        # Create and save additional options
        for option_text in option_texts:
            if option_text:
                answer_option = Answer(question=form.cleaned_data['question'], text=option_text)
                answer_option.save()

        return super().form_valid(form)
    

class QuesAnsImageView(CreateView):
    template_name = "quesansimage.html"
    model = AnswerImages
    form_class = QuesAnsFormImg
    success_url = reverse_lazy('qimg')

    def form_valid(self, form):
        # Save the main answer
        main_answer = form.save(commit=False)
        main_answer.save()

        # Handle file uploads for options
        for i in range(1, 4):
            option_file = self.request.FILES.get(f'option_{i}')
            if option_file:
                AnswerImages.objects.create(
                    question=main_answer.question,
                    fileans=option_file
                )

        return super().form_valid(form)
    
class QuesAnsAudioView(CreateView):
    template_name="quesansaudio.html"
    model=AnswerAudio
    form_class=QuesAnsFormAudio
    success_url=reverse_lazy('qaudio') 
    def form_valid(self, form):
        # Save the main answer
        main_answer = form.save(commit=False)
        main_answer.save()

        # Handle file uploads for options
        for i in range(1, 4):
            option_file = self.request.FILES.get(f'option_{i}')
            if option_file:
                AnswerAudio.objects.create(
                    question=main_answer.question,
                    fileans=option_file
                )

        return super().form_valid(form)
    

class DeleteView(View):
    def get(self,req,*args,**kwargs):
       id=kwargs.get('pk')
       dl=Question.objects.get(id=id)
       dl.delete()
       return redirect('qdel')
    

class DeleteImgView(View):
    def get(self,req,*args,**kwargs):
       id=kwargs.get('pk')
       dl=QuestionImages.objects.get(id=id)
       dl.delete()
       return redirect('qimg')
    

class DeleteAudioView(View):
    def get(self,req,*args,**kwargs):
       id=kwargs.get('pk')
       dl=QuestionAudio.objects.get(id=id)
       dl.delete()
       return redirect('qaudio')
    
# class Quesdel(TemplateView):
#     template_name="quesdel.html"
#     def get_context_data(self, **kwargs) :
#         context = super().get_context_data(**kwargs)
#         context['tests']=Question.objects.all()
#         return context

class SugView(TemplateView):
    template_name="suggestions.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data']=Suggestion.objects.all().order_by('cat')
        return context

class SuggTextView(CreateView):
    template_name="suggtext.html"
    model=Suggestion
    form_class=SugForm
    success_url=reverse_lazy('st')



class SuggVideoView(CreateView):
    template_name="suggvideo.html"
    model=Suggestion
    form_class=SugVideoForm
    success_url=reverse_lazy('sv')

class SuggAudioView(CreateView):
    template_name="suggaudio.html"
    model=Suggestion
    form_class=SugAudioForm
    success_url=reverse_lazy('sadd')




def view_video(request, video_id):
    video = get_object_or_404(Suggestion, pk=video_id)
    video_path = video.video.path
    response = FileResponse(open(video_path, 'rb'))  # Adjust content_type as needed
    return response


def view_videoo(request, videoo_id):
    video = get_object_or_404(ScoreModel, pk=videoo_id)
    video_path = video.video.path
    response = FileResponse(open(video_path, 'rb'))  # Adjust content_type as needed
    return response




def play_audio(request, audio_id):
    audio_recording = get_object_or_404(Suggestion, pk=audio_id)
    audio_file = audio_recording.audio
    response = FileResponse(open(audio_file.path, 'rb'))
    return response

def play_audioo(request, audio_id):
    audio_recording = get_object_or_404(ScoreModel, pk=audio_id)
    audio_file = audio_recording.audio
    response = FileResponse(open(audio_file.path, 'rb'))
    return response


class DeleteViewSug(View):
    def get(self,req,*args,**kwargs):
       id=kwargs.get('pk')
       dl=Suggestion.objects.get(id=id)
       dl.delete()
       return redirect('sadd')
    

class ChangePasswordViewHome(FormView):
    template_name="changepshome.html"
    form_class=ChangePasswordForm
    def post(self,request,*args,**kwargs):
        form_data=ChangePasswordForm(data=request.POST)
        if form_data.is_valid():
            current=form_data.cleaned_data.get("current_password")
            new=form_data.cleaned_data.get("new_password")
            confirm=form_data.cleaned_data.get("confirm_password")
            user=authenticate(request,username=request.user.username,password=current)
            if user:
                if new==confirm:
                    user.set_password(new)
                    user.save()
                    logout(request)
                    return redirect("log")
                else:
                    return redirect("cp")
            else:
                return redirect("cp")
        else:
            return render(request,"changepassword.html",{"form":form_data})    
        

class SuggestionUpdateView(UpdateView):
    template_name='suggestionupdate.html'
    model=Suggestion
    form_class=SuggestionForm
    success_url=reverse_lazy('sadd')        



