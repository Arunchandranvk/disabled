from typing import Any
from django.shortcuts import render,redirect
from django.views.generic import TemplateView,CreateView,View
from accounts.models import *
from django.db.models import Q
from .models import Notes,ViewedMessages
from .forms import *
from django.urls import reverse_lazy
from django.core.mail import send_mail
import pandas as pd
import random
# Create your views here.



class HomeView(TemplateView):
    template_name="home.html"


class StudentsView(TemplateView):
    template_name="students.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data']=Student.objects.all().order_by('std_id')
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
     template_name='detail.html'
     def get_context_data(self, **kwargs):
          context = super().get_context_data(**kwargs)    
          id=kwargs.get('pk') 
          context['data']=Student.objects.get(id=id)
          context['det']=ScoreModel.objects.filter(student=id)
          return context
     
class Score_view(TemplateView):
     template_name='testscore.html'
     def get_context_data(self, **kwargs):
          context = super().get_context_data(**kwargs)
          context['data']=Student.objects.all().order_by('std_id')
          context['que']=Question.objects.all()
          query=self.request.GET.get('query')
          if query:   
             context["searchs"]=StudentAnswer.objects.filter(Q( student=query) )
          else :
               None   
          return context
     
class Ques(TemplateView):
    template_name="questions.html"     
     
     

class SD(TemplateView):
    template_name='student_details.html'
    def get_context_data(self, **kwargs):
          context = super().get_context_data(**kwargs)
          id=kwargs.get('pk')
          print(id)
          context['st']=Student.objects.get(id=id)
          context['data']=StudentAnswer.objects.filter(student=id)
        #   context['dataimg']=StudentAnswerImage.objects.filter(student=id)
          context['dataaudio']=StudentAnswerAudio.objects.filter(student=id)
          context['file']=ScoreModel.objects.filter(student=id)
          print(context)
          return context
    
class NotesView(CreateView):
     template_name='notes.html'
     model=Notes
     form_class=NotesForm
     success_url=reverse_lazy('note')
     print("count====",Question.objects.all().count())
     def get_context_data(self, **kwargs):
          context = super().get_context_data(**kwargs)
          context['data']=Notes.objects.all().order_by('-dt')
          return context
     def form_valid(self, form):
        # Get the admin user or modify this part based on your user retrieval logic
        admin_user = CustUser.objects.get(username='admin')

        # Customize this method to send an email based on the user's category
        for user in Student.objects.filter(disability=form.cleaned_data['cat']):
            subject = f'New Note Added - {form.cleaned_data["cat"]}'
            message = f'A new note has been added in the {form.cleaned_data["cat"]} category.'
            from_email = 'donkannukkadan@gmail.com'  # Replace with your admin email
            to_email = [user.email]

            send_mail(subject, message, from_email, to_email, fail_silently=False)

        # Call the original form_valid method to save the form data
        response = super().form_valid(form)

        return response


class DeleteViewNotes(View):
    def get(self,req,*args,**kwargs):
       id=kwargs.get('pk')
       dl=Notes.objects.get(id=id)
       dl.delete()
       return redirect('note')

class DeleteViewExamDetails(View):
    def get(self,req,*args,**kwargs):
    #    user=req.user.id
    #    print(user)
       id=kwargs.get('pk')
       print(id)
       dl=StudentAnswer.objects.filter(student=id)
       dl.delete()
       return redirect('score')

class DeleteViewExamDetailsAudio(View):
    def get(self,req,*args,**kwargs):
    #    user=req.user.id
    #    print(user)
       id=kwargs.get('pk')
       print(id)
       dl=StudentAnswerAudio.objects.filter(student=id)
       dl.delete()
       return redirect('score')
    

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