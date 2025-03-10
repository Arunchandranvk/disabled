from typing import Any
from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import TemplateView,CreateView,View,UpdateView
from accounts.models import *
from django.db.models import Q
from .models import Notes,ViewedMessages
from .forms import *
from django.urls import reverse_lazy
from django.core.mail import send_mail
import random
from django.http import HttpResponse,JsonResponse
from django.contrib import messages
# Create your views here.



class HomeView(TemplateView):
    template_name="home.html"


class StudentsView(TemplateView):
    template_name="students.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user=self.request.user
        try:
            fac=Class_Name.objects.get(faculty=user)
            context['data'] = Student.objects.filter(class_id=fac.id).order_by('std_id')
        except Class_Name.DoesNotExist:
            context['error'] = "No matching class found for the faculty."
        except Exception as e:
            context['error'] = str(e)
        return context

class Questionadd(CreateView):
    template_name="questions.html"
    model=ExamQuestions
    form_class=QuestionsForm
    def get_success_url(self):
        return reverse_lazy('question', kwargs={'pk': self.kwargs['pk']})
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        exam_id=self.kwargs.get('pk')
        exam=Exam.objects.get(id=exam_id)
        kwargs['exam']=exam.id
        return kwargs
    def get_context_data(self, **kwargs) :
        context = super().get_context_data(**kwargs)
        exam_id=self.kwargs.get('pk') 
        print(exam_id)
        exam=Exam.objects.get(id=exam_id)
        context['exam']=exam
        context['ques'] = ExamQuestions.objects.filter(exam=exam.id)
        return context

class QuestionUpdateView(UpdateView):
    template_name="question_update.html"
    model=ExamQuestions
    form_class=QuestionsForm
    def get_success_url(self):
        question = self.get_object()
        return reverse_lazy('question', kwargs={'pk': question.exam.id})


def QuestionDeleteView(request, question_id):
    try:
        question = get_object_or_404(ExamQuestions, id=question_id)
        question.delete()
        return redirect('question',pk=question.exam.id)  
    except Exception as e:
        return redirect('question',pk=question.exam.id) 


def ExamDeleteView(request, exam_id):
    try:
        exam = get_object_or_404(Exam, id=exam_id)
        exam.delete()
        return redirect('exam-name')  
    except Exception as e:
        return redirect('exam-name') 
    


class ExamCreate(CreateView):
    template_name="exam_create.html"
    model=Exam
    form_class=ExamNameForm
    success_url=reverse_lazy('exam-name')
    def get_context_data(self, **kwargs) :
        context = super().get_context_data(**kwargs) 
        context['exams'] = Exam.objects.filter(faculty=self.request.user).order_by('-date')
        return context


class Search(TemplateView):
    template_name="d_search.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query=self.request.GET.get('query')
        if query:
               context["data"]=Student.objects.filter(Q( std_id__icontains=query) )
        # context['search']=Product.objects.get('query')
        return context     
    
class DetailView(TemplateView):
     template_name='student_detail.html'
     def get_context_data(self, **kwargs):
          context = super().get_context_data(**kwargs)    
          id=kwargs.get('pk') 
          context['data']=Student.objects.get(id=id)
          context['det']=ScoreModel.objects.filter(student=id)
          return context
     
class ExamDetailsview(TemplateView):
     template_name='exam_details.html'
     def get_context_data(self, **kwargs):
          context = super().get_context_data(**kwargs)
          context['exams']=Exam.objects.filter(faculty=self.request.user.id).order_by('-date')
          return context
     
class StudentExamDetailsview(TemplateView):
    template_name = 'student_examdetails.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        exam_id = kwargs.get('pk')
        user = self.request.user
        fac = Class_Name.objects.get(faculty=user)
        ex = AssignExam.objects.get(faculty=user.id,exam=exam_id)
        # print(ex)
        students = Student.objects.filter(class_id=fac.id).order_by('std_id')
        scores = ScoreModel.objects.filter(assignedexam=ex)
        print(scores)
        scores_dict = {score.student_id: score for score in scores}
        combined_data = []
        for student in students:
            student_data = {
                "std_id": student.std_id,
                "student_name": student.student_name,
                "class_name": student.class_id.class_name,
                "score": scores_dict.get(student.id).score if student.id in scores_dict else "N/A",
                "category": scores_dict.get(student.id).cat.name if student.id in scores_dict and scores_dict[student.id].cat else "N/A",
                "img": student.img.url if student.img else None,
            }
            combined_data.append(student_data)

        context['combined_data'] = combined_data
        return context




def AssignExamView(request, exam_id):
    try:
        faculty = request.user.id
        exam = get_object_or_404(Exam, id=exam_id)
        if exam.is_active:
            messages.warning(request, "The exam is already active.")
            return redirect('exam-detail')  
        
        examques = ExamQuestions.objects.filter(exam=exam)
        if not examques.exists():
            messages.error(request, "The exam has no questions. Please add questions before assigning.")
            return redirect('exam-name')
        class_id = Class_Name.objects.get(faculty=faculty)
        fac = get_object_or_404(Faculty, id=faculty)
        AssignExam.objects.create(faculty=fac, exam=exam, class_id=class_id)
        
        exam.is_active = True
        exam.save()
        
        messages.success(request, "The exam has been successfully assigned and activated.")
        return redirect('exam-detail')  
    
    except Class_Name.DoesNotExist:
        messages.error(request, "You are not associated with any class.")
        return redirect('exam-name') 
    
    except Exception as e:
        messages.error(request, f"An unexpected error occurred: {str(e)}")
        return redirect('exam-name') 

def DeactivateExamView(request,exam_id):
    try:
        exam = get_object_or_404(Exam, id=exam_id)
        assign = AssignExam.objects.get(exam=exam)
        assign.delete()
        exam.is_active=False
        exam.save()
        return redirect('exam-detail')
    except Exception as e:
        messages.error(request, f"An unexpected error occurred: {str(e)}")
        return redirect('exam-detail')
     

class NotesView(CreateView):
    template_name = 'notes.html'
    model = Notes
    form_class = NotesForm
    success_url = reverse_lazy('note')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['notes'] = Notes.objects.filter(user=self.request.user).order_by('-dt')
        return context


    def form_valid(self, form):
        response = super().form_valid(form)

        return response


class DeleteViewNotes(View):
    def get(self,req,*args,**kwargs):
       id=kwargs.get('pk')
       dl=Notes.objects.get(id=id)
       dl.delete()
       return redirect('note')

    

class MessageView(CreateView):
    template_name='messages.html'
    model=Messages
    form_class=MessageForm
    success_url=reverse_lazy('msg')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data']=Messages.objects.all()
        return context

    

class MsgViewed(TemplateView):
    template_name='msg_viewedby.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id=kwargs.get('pk')
        context['msg']=ViewedMessages.objects.filter(msg=id)
        return context