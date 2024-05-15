from typing import Any
from django.shortcuts import render,redirect,HttpResponse
from django.views.generic import FormView,TemplateView,UpdateView,View
from accounts.forms import *
from .forms import *
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse_lazy
from django.contrib import messages
from home.models import *
# Create your views here.
from django.shortcuts import render
from django.http import JsonResponse
from PyPDF2 import PdfReader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
import os
from django.views.decorators.csrf import csrf_exempt
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain import PromptTemplate

@csrf_exempt
def chatbot_view(request):
    if request.method == 'POST':
        openai_api_key = 'api_key'
        llm = OpenAI(openai_api_key=openai_api_key, temperature=0.8)

        input_text = request.POST.get('input_text', '')

        if input_text.lower() == 'exit':
            return JsonResponse({'response': 'Thank you for using Chatbot. Have a great day ahead'})

        if input_text.lower() in ['hi', 'hai', 'hello', 'hy']:
            return JsonResponse({'response': 'Hai, Welcome to Chatbot'})

        if input_text.lower() in ['bye', 'by', 'goodbye', 'thank you', 'thanks']:
            return JsonResponse({'response': 'Thank you for using Chatbot. Have a great day ahead.'})

        input_prompt = PromptTemplate(input_variables=['query'], template='IT related {query}')
        chain = LLMChain(llm=llm, prompt=input_prompt, verbose=True)
        
        return JsonResponse({'response': chain.run(input_text)})
    else:
        return JsonResponse({'response': 'Invalid request'}, status=400)


class ChatBotView(TemplateView):
    template_name="chatbot.html"



class StuHomeView(TemplateView):
    template_name='sthome.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user=self.request.user.id
        print(user)
        context['data']=Student.objects.get(id=user)
        return context

import random
def studentanswer(request,**kwargs):
    if request.user.is_authenticated:
        student = request.user.student_id_id  
        student_answers = list(StudentAnswer.objects.filter(student=student))
        random.shuffle(student_answers)
        
        num = range(1, 11)
        return render(request, 'exam.html', {'student_answers': student_answers,"num":num})

    elif not student_answers:
       
        return render(request, 'exam.html')

def studentanswer_audio(request,**kwargs):
    if request.user.is_authenticated:
        student = request.user.student_id.id 
        print(student)
        student_answers = StudentAnswerAudio.objects.filter(student=student)
        ans=AnswerAudio.objects.all()
        quecount=student_answers.count()
        print("hii",student_answers.count())
        # print(student_answers)
        # for index, student_answer in enumerate(student_answers, start=1):
            # print(f"Iteration ID: {index} - Question File: {student_answer.question.files}")
    
            # for j_index, j in enumerate(AnswerAudio.objects.filter(question=student_answer.question.id), start=1):
                # print(f'Iteration ID: {index}.{j_index} ======== Answer File: {j.fileans}')



        return render(request, 'exam2.html', {'student_answers': student_answers,'ans':ans,"count":quecount})

    elif not student_answers:
       
        return render(request, 'exam2.html')

def studentanswer_image(request,**kwargs):
    if request.user.is_authenticated:
        student = request.user.student_id  
        student_answers = StudentAnswerImage.objects.filter(student=student)
        ans=AnswerImages.objects.all()
        num = range(1, 11)
        return render(request, 'exam3.html', {'student_answers': student_answers,"ans":ans})

    elif not student_answers:
       
        return render(request, 'exam3.html')


from django.shortcuts import get_object_or_404
 
def submit_exam(request): 
    student = request.user.id 
    if ScoreModel.objects.filter(student=student, score__isnull=False).exists(): 
        messages.error(request,"Exam Already Attended!!!!!!") 
        return render(request, 'exam.html') 
    elif request.method == 'POST': 
        student = get_object_or_404(Student, pk=student)  
        print(student)
        count=Question.objects.all().count()

        stu = ScoreModel.objects.create(student=student)
        total_score = 0
        for key, value in request.POST.items():
            if key.startswith('answer_'):
                student_answer_id = int(key.split('_')[1])
                answer_id = int(value)
                student_answer = StudentAnswer.objects.get(id=student_answer_id)
                student_answer.answer_id = answer_id
                student_answer.save()
                if student_answer.answer_id == answer_id and student_answer.answer.is_correct:
                        total_score += 1
            sug=Suggestion.objects.all()
            if total_score >= count-1:
                category_instance = get_object_or_404(Categorys, pk=5)
                stu.cat = category_instance
                for i in sug:
                   if i.cat.name == "Excellent":
                      stu.suggestion= i.suggestion
                      stu.video=i.video
                      stu.audio=i.audio
            elif total_score >= count-3:
                category_instance = get_object_or_404(Categorys, pk=4)
                stu.cat = category_instance
                for i in sug:
                   if i.cat.name == "Good":
                    stu.suggestion= i.suggestion
                    stu.video=i.video
                    stu.audio=i.audio
            elif total_score>= count-4:
                category_instance = get_object_or_404(Categorys, pk=3)
                stu.cat = category_instance
                for i in sug:
                   if i.cat.name == "Average":
                    stu.suggestion= i.suggestion
                    stu.video=i.video
                    stu.audio=i.audio
            elif total_score >= count-5:
                category_instance = get_object_or_404(Categorys, pk=2)
                stu.cat = category_instance
                for i in sug:
                   if i.cat.name == "Poor":
                    stu.suggestion= i.suggestion
                    stu.video=i.video
                    stu.audio=i.audio
            else:
                category_instance = get_object_or_404(Categorys, pk=1)
                stu.cat = category_instance
                for i in sug:
                   if i.cat.name == "Very Poor":
                        stu.suggestion= i.suggestion
                        stu.video=i.video
                        stu.audio=i.audio            
            stu.score = total_score
            stu.save()
            
        return redirect('sh') 
    else:
        return HttpResponse("Invalid request method.", status=405)

def submit_exam_audio(request):
    student = request.user.id
    if ScoreModel.objects.filter(student=student, score__isnull=False).exists():
        messages.error(request,"Exam Already Attended!!!!!!")
        return render(request, 'exam2.html') 
    elif request.method == 'POST':
        student = get_object_or_404(Student, pk=student)  
        print(student)
        count=QuestionAudio.objects.all().count()
        print(count)
        print(count-1)
        stu = ScoreModel.objects.create(student=student)
        total_score = 0
        for key, value in request.POST.items():
            if key.startswith('answer_'):
                student_answer_id = int(key.split('_')[1])
                answer_id = int(value)
                student_answer = StudentAnswerAudio.objects.get(id=student_answer_id)
                student_answer.answer_id = answer_id
                student_answer.save()
                if student_answer.answer_id == answer_id and student_answer.answer.is_correct:
                        total_score += 1
            sug=Suggestion.objects.all()
            if total_score >= count-1:
                category_instance = get_object_or_404(Categorys, pk=5)
                stu.cat = category_instance
                for i in sug:
                   if i.cat.name == "Excellent":
                      stu.suggestion= i.suggestion
                      stu.video=i.video
                      stu.audio=i.audio
            elif total_score >= count-3:
                category_instance = get_object_or_404(Categorys, pk=4)
                stu.cat = category_instance
                for i in sug:
                   if i.cat.name == "Good":
                    stu.suggestion= i.suggestion
                    stu.video=i.video
                    stu.audio=i.audio
            elif total_score>= count-4:
                category_instance = get_object_or_404(Categorys, pk=3)
                stu.cat = category_instance
                for i in sug:
                   if i.cat.name == "Average":
                    stu.suggestion= i.suggestion
                    stu.video=i.video
                    stu.audio=i.audio
            elif total_score >= count-5:
                category_instance = get_object_or_404(Categorys, pk=2)
                stu.cat = category_instance
                for i in sug:
                   if i.cat.name == "Poor":
                    stu.suggestion= i.suggestion
                    stu.video=i.video
                    stu.audio=i.audio
            else:
                category_instance = get_object_or_404(Categorys, pk=1)
                # print(category_instance)

                stu.cat = category_instance
                # print(category_instance)
                for i in sug:
                   if i.cat.name == "Very Poor":
                        stu.suggestion= i.suggestion
                        stu.video=i.video
                        stu.audio=i.audio            
            stu.score = total_score
            stu.save()
            
        return redirect('res',pk=request.user.id) 
    else:
        return HttpResponse("Invalid request method.", status=405)

def submit_exam_image(request):
    student = request.user.id
    if ScoreModel.objects.filter(student=student, score__isnull=False).exists():
        messages.error(request,"Exam Already Attended!!!!!!")
        return render(request, 'exam3.html') 
    elif request.method == 'POST':
        student = get_object_or_404(Student, pk=student)  
        print(student)
        count=QuestionImages.objects.all().count()

        stu = ScoreModel.objects.create(student=student)
        total_score = 0
        for key, value in request.POST.items():
            if key.startswith('answer_'):
                student_answer_id = int(key.split('_')[1])
                answer_id = int(value)
                student_answer = StudentAnswerImage.objects.get(id=student_answer_id)
                student_answer.answer_id = answer_id
                student_answer.save()
                if student_answer.answer_id == answer_id and student_answer.answer.is_correct:
                        total_score += 1
            sug=Suggestion.objects.all()
            if total_score >= count-1:
                category_instance = get_object_or_404(Categorys, pk=5)
                stu.cat = category_instance
                for i in sug:
                   if i.cat.name == "Excellent":
                      stu.suggestion= i.suggestion
                      stu.video=i.video
                      stu.audio=i.audio
            elif total_score >= count-3:
                category_instance = get_object_or_404(Categorys, pk=4)
                stu.cat = category_instance
                for i in sug:
                   if i.cat.name == "Good":
                    stu.suggestion= i.suggestion
                    stu.video=i.video
                    stu.audio=i.audio
            elif total_score>= count-4:
                category_instance = get_object_or_404(Categorys, pk=3)
                stu.cat = category_instance
                for i in sug:
                   if i.cat.name == "Average":
                    stu.suggestion= i.suggestion
                    stu.video=i.video
                    stu.audio=i.audio
            elif total_score >= count-5:
                category_instance = get_object_or_404(Categorys, pk=2)
                stu.cat = category_instance
                for i in sug:
                   if i.cat.name == "Poor":
                    stu.suggestion= i.suggestion
                    stu.video=i.video
                    stu.audio=i.audio
            else:
                category_instance = get_object_or_404(Categorys, pk=1)
                stu.cat = category_instance
                for i in sug:
                   if i.cat.name == "Very Poor":
                        stu.suggestion= i.suggestion
                        stu.video=i.video
                        stu.audio=i.audio            
            stu.score = total_score
            stu.save()
            
        return redirect('sh') 
    else:
        return HttpResponse("Invalid request method.", status=405)


class Profile(TemplateView):
   template_name='profile.html'
   def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs) 
      id=self.request.user
      context['data']=Student.objects.get(std_id=id)
      return context
   
class ProfileUpdateView(UpdateView):
    template_name="profileupdate.html"
    model=Student
    form_class=StudentFormProfile
    success_url=reverse_lazy('pro')


class SugView(TemplateView):
   template_name='sugg.html'
   def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs) 
      id=self.request.user.id
      context['data']=ScoreModel.objects.filter(student=id)
      context['data1']=Student.objects.get(id=id)
      return context
   
class ResultView(TemplateView):
   template_name='result.html'
   def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs) 
      id=kwargs.get('pk')
      print(id)
      student = get_object_or_404(Student, id=id)
    #   context['st']=student.objects.get(id=id)
      context['data'] = ScoreModel.objects.filter(student=student).first()
      context['result']=StudentAnswer.objects.filter(student=id)
      context['resultimg']=StudentAnswerImage.objects.filter(student=id)
      context['resultaudio']=StudentAnswerAudio.objects.filter(student=id)
      return context



class ChangePasswordView(FormView):
    template_name="changeps.html"
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
        
class LogOut(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect("log")      
    

class Text(TemplateView):
    template_name="text.html"    
    def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs) 
      id=self.request.user.id
      context['data']=ScoreModel.objects.filter(student=id)
      return context
    
class Audio(TemplateView):
    template_name="audio.html"    
    def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs) 
      id=self.request.user.id
      context['data']=ScoreModel.objects.filter(student=id)
      context['data1']=Student.objects.get(id=id)
      return context



class NotesListView(TemplateView):
    template_name='notesview.html'    
    def get_context_data(self, **kwargs):
          context = super().get_context_data(**kwargs)
          id=kwargs.get('pk')
          data=Notes.objects.all().order_by('-dt')
          
          context['data']=Notes.objects.all().order_by('-dt')
       
          context['user']=Student.objects.filter(id=id)
        #   play_audio(context)
          return context
    

import speech_recognition as sr

def voice_recognition(request):
    recognizer = sr.Recognizer()
    
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
    
    try:
        # Convert audio to text
        text = recognizer.recognize_google(audio)
        print("You said:", text)
        pk=request.user.student_id.id
        # Implement logic based on recognized text
        if "go to home page" in text.lower():
            return redirect('sh')  # Redirect to home page
        elif "go to profile" in text.lower():
            return redirect('pro')  # Redirect to about page
        elif "go to update profile" in text.lower():
            return redirect('proupd',pk=pk)  # Redirect to about page
        elif "go to exam" in text.lower():
            return redirect('ansaudio')  # Redirect to about page
        elif "go to suggestions" in text.lower():
            return redirect('sug')  # Redirect to about page
        elif "go to audio" in text.lower():
            return redirect('audio')  # Redirect to about page

        elif "go to result" in text.lower():
            return redirect('res',pk=pk)  # Redirect to about page
        elif "logout" in text.lower():
            return redirect('logout')  # Redirect to about page
        elif "go to change password" in text.lower():
            return redirect('cp')  # Redirect to about page
        elif "go to games" in text.lower():
            return redirect('game')  # Redirect to about page
        elif "go to explore more" in text.lower():
            
            return redirect('noteview',pk=pk)  # Redirect to about page
        # Add more conditions for other pages
        
    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError as e:
        print("Error: {0}".format(e))
    
    # If no recognized command or error, stay on the same page or redirect somewhere else
    return redirect('sh') 
   
from home.models import *

class MessageGetView(TemplateView):
    template_name='studentmsg.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_messages = Messages.objects.all()
        
        # Get IDs of messages viewed by the current user
        viewed_message_ids = set(ViewedMessages.objects.filter(user=self.request.user, viewed=True).values_list('msg__id', flat=True))
        
        # Mark messages as viewed if they haven't been viewed already
        for message in all_messages:
            if message.id not in viewed_message_ids:
                ViewedMessages.objects.create(msg=message, user=self.request.user, viewed=True)
        
        # Pass all messages to the template
        context['data'] = all_messages
        return context