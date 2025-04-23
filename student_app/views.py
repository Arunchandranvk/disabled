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

import os


class ExamDetailView(View):
    def get(self, request, exam_id):
        exam = Exam.objects.get(id=exam_id)
        if not exam.is_active:
            return redirect('exams')

        questions = ExamQuestions.objects.filter(exam=exam)
        context = {
            'exam': exam,
            'questions': questions,
        }
        return render(request, 'main_exam.html', context)

    def post(self, request, exam_id):
        # Get exam and related information
        exam = Exam.objects.get(id=exam_id)
        stu = request.user
        questions = ExamQuestions.objects.filter(exam=exam)
        count = questions.count()
        assigned_exam = AssignExam.objects.get(exam=exam)
        student = get_object_or_404(Student, id=stu.id)
        total_score = exam.total_score
        score = 0

        for question in questions:
            answer = request.POST.get(f'q{question.id}')
            is_correct = answer == question.answer

            if is_correct:
                score += total_score / count 
            ExamResult.objects.get_or_create(
                assignedexam=assigned_exam,
                student=student,
                question=question,
                ans=answer,
                is_correct=is_correct
            )
        exce = total_score / 5
        category_id = min(int(score // exce) + 1, 5) 
        cat = Categorys.objects.get(id=category_id)
        ScoreModel.objects.get_or_create(
            assignedexam=assigned_exam,
            student=student,
            score=score,
            cat=cat
        )
        HistoryExam.objects.get_or_create(
            assignedexam=assigned_exam,
            student=student,
            score=score,
            cat=cat
        )
        return redirect('res', pk=exam.id)

class ChatBotView(TemplateView):
    template_name="chatbot.html"


class AssignedExamStudentPageView(TemplateView):
    template_name = 'assigned_exam.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user.id
        student = Student.objects.get(id=user)        
        all_exams = Exam.objects.filter(
            faculty=student.class_id.faculty,
            is_active=True
        )      
        taken_exam_ids = ScoreModel.objects.filter(
            student=student
        ).values_list('assignedexam__exam_id', flat=True)
        context['exams'] = all_exams.exclude(id__in=taken_exam_ids)
        return context



class ResultStudentPageView(TemplateView):
    template_name = 'result_of_exams.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user.id
        student = Student.objects.get(id=user)        
        context['exams'] = ScoreModel.objects.filter(
            student=student,
            assignedexam__faculty=student.class_id.faculty
        ).select_related('assignedexam', 'assignedexam__exam')
        
        return context


class StuHomeView(TemplateView):
    template_name='sthome.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user=self.request.user.id
        print(user)
        context['data']=Student.objects.get(id=user)
        return context



from django.shortcuts import get_object_or_404
 
class Profile(TemplateView):
   template_name='profile.html'
   def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs) 
      id=self.request.user.id
      context['data']=Student.objects.get(id=id)
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
      stu = Student.objects.get(id=id)
      print(stu)
      print(ScoreModel.objects.filter(student=stu.id))

      context['data']=ScoreModel.objects.filter(student=stu.id)

      return context
   
class ResultView(TemplateView):
    template_name = 'result.html'

    def get(self, request, *args, **kwargs):
        try:
            id = kwargs.get('pk')
            exam_id = get_object_or_404(Exam, id=id)
            student = get_object_or_404(Student, id=self.request.user.id)
            assign = AssignExam.objects.get(
                faculty=exam_id.faculty,
                exam=exam_id,
                class_id=student.class_id
            )
            ScoreModel.objects.get(student=student, assignedexam=assign)

        except ScoreModel.DoesNotExist:
            messages.error(self.request, "No Result Found!")
            return redirect('result')  # Replace 'result' with your fallback page name
        except AssignExam.DoesNotExist:
            messages.error(self.request, "No assigned exam found!")
            return redirect('result')

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id = kwargs.get('pk')
        exam_id = get_object_or_404(Exam, id=id)
        student = get_object_or_404(Student, id=self.request.user.id)
        assign = AssignExam.objects.get(
            faculty=exam_id.faculty,
            exam=exam_id,
            class_id=student.class_id
        )
        context['assigned'] = assign
        context['data'] = ScoreModel.objects.get(student=student, assignedexam=assign)
        context['result'] = ExamResult.objects.filter(student=student.id, assignedexam=assign)
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
          context['notes']=Notes.objects.all().order_by('-dt')
          return context
    
   
from home.models import *

class MessageGetView(TemplateView):
    template_name='studentmsg.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_messages = Messages.objects.all()
        viewed_message_ids = set(ViewedMessages.objects.filter(user=self.request.user, viewed=True).values_list('msg__id', flat=True))
        for message in all_messages:
            if message.id not in viewed_message_ids:
                ViewedMessages.objects.create(msg=message, user=self.request.user, viewed=True)
        context['data'] = all_messages
        return context
    
    
    
import re
import groq
    
client = groq.Client(api_key="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")


def get_groq_response(user_input):
    """
    Communicate with the GROQ chatbot to get a response based on user input.
    """
    system_prompt = {
        "role": "system",
        "content": "You are a helpful assistant."
    }

    chat_history = [system_prompt]

    # Append user input to the chat history
    chat_history.append({"role": "user", "content": user_input})

    # Get response from GROQ API
    chat_completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=chat_history,
        max_tokens=100,
        temperature=1.2
    )

    response = chat_completion.choices[0].message.content
    print(response)
    # Format response (convert *bold* to <b>bold</b>)
    response = re.sub(r'\\(.?)\\*', r'<b>\1</b>', response)

    return response

import json
from django.http import JsonResponse

class ChatbotView(View):
    def get(self, request):
        return render(request, "chatbot.html")
    def post(self, request): 
        try:
            body = json.loads(request.body)
            user_input = body.get('userInput')
        except json.JSONDecodeError as e:
            return JsonResponse({"error": "Invalid JSON format."})
    
        if not user_input:  # If user_input is None or empty
            print("no")
            return JsonResponse({"error": "No user input provided."})  
        
        print("User Input:", user_input)
        
        static_responses = {
            "hi": "Hello! How can I assist you today?",
            "hello": "Hi there! How can I help you?",
            "how are you": "I'm just a chatbot, but I'm doing great! How about you?",
            "bye": "Goodbye! Take care.",
            "whats up": "Not much, just here to help you with  queries. How can I help you today?",
        }

        lower_input = user_input.lower().strip()
        if lower_input in static_responses:
            print(static_responses[lower_input])
            return JsonResponse({'response': static_responses[lower_input]})
        
        try:
            print("Processing via GROQ")
            data = get_groq_response(user_input)
            print(data)
            treatment_list = data.split('\n')
            return JsonResponse({'response': treatment_list})
        except Exception as e:
            return JsonResponse({"error": f"Failed to get GROQ response: {str(e)}"})