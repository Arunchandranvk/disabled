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
        print(questions)
        context = {
            'exam': exam,
            'questions': questions,
        }
        return render(request, 'main_exam.html', context)

    def post(self, request, exam_id):
        exam = Exam.objects.get(id=exam_id)
        stu = request.user
        questions = ExamQuestions.objects.filter(exam=exam)
        count = questions.count()
        assigned_exam = AssignExam.objects.get(exam=exam)
        student = get_object_or_404(Student,id=stu.id)
        total = exam.total_score
        score = 0
        print(questions)
        for question in questions:
            
            answer = request.POST.get(f'q{question.id}')
            is_correct = answer == question.answer
            
            if is_correct:
                score += total/count
                
            ExamResult.objects.get_or_create(
                assignedexam=assigned_exam,
                student=student,
                question=question,
                ans=answer,
                is_correct=is_correct
            )
        exce = exam.total_score/5
        if score <= exce:
            cat = Categorys.objects.get(id=1)
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

        elif score <= (exce*2):
            cat = Categorys.objects.get(id=2)
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
        elif score <= (exce*3):
            cat = Categorys.objects.get(id=3)
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
        elif score <= (exce*4):
            cat = Categorys.objects.get(id=4)
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
        elif score <= (exce*5):
            cat = Categorys.objects.get(id=5)
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