from typing import Any
from django.shortcuts import render,redirect
from .models import *
from .forms import *
from django.views.generic import FormView,CreateView,UpdateView,TemplateView,View
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse_lazy
from student_app.forms import ChangePasswordForm
from django.db.models.signals import post_save
from django.http import JsonResponse
import os
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import logout as auth_logout
from .face_recognition import *
from django.core.files.base import ContentFile
import base64
from home.models import *


def custom_logout(request):
    auth_logout(request)
    return redirect('log')


class MainHome(TemplateView):
    template_name="mainhome.html"


class ClearDataView(View):
    def post(self, request):
        # StudentAnswer.objects.all().delete()
        # StudentAnswerImage.objects.all().delete()
        # StudentAnswerAudio.objects.all().delete()
        # ScoreModel.objects.all().delete()
        return JsonResponse({'message': 'Data cleared successfully'})


# @receiver(post_save, sender=Student)
# def create_user_from_student(sender, instance, created, **kwargs):
#     if created:
#         CustUser= get_user_model()
#         student_id_id=instance.id
#         username = instance.std_id
#         password = 'admin@123' 
#         CustUser.objects.create_user(email=username, password=password,student_id_id=student_id_id)

def face_login_view(request):
    """
    Handle face login with captured image
    """
    if request.method == 'POST' and request.POST.get('face_image'):
        try:
            face_image_data = request.POST.get('face_image')

            format, imgstr = face_image_data.split(';base64,')
            ext = format.split('/')[-1]
            image_data = ContentFile(base64.b64decode(imgstr), name=f'captured_image.{ext}')

            fs = FileSystemStorage()
            filename = fs.save(image_data.name, image_data)
            file_path = fs.path(filename)

            face_recognizer = FaceRecognition()
            
            username_with_extension = face_recognizer.authenticate_by_face(file_path)
            username = os.path.splitext(username_with_extension)[0]
            print("username",username)
            os.remove(file_path)

            if username:
                user = Student.objects.get(std_id=username)
                login(request, user)
                return redirect('sh')  # Redirect to home page
            else:
                
                messages.error(request, 'Face not recognized. Please try again.')
                return redirect('face_login')

        except Exception as e:
            # Log the error and show a generic error message
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Face login error: {str(e)}")
            
            from django.contrib import messages
            messages.error(request, 'An error occurred during login. Please try again.')
            return redirect('face_login')

    # Render the login page for GET requests
    return render(request, 'face_login.html')


class LoginViewFaculty(FormView):
    template_name="login.html"
    form_class=LogForm
    def post(self,request,*args,**kwargs):
        log_form=LogForm(data=request.POST)
        if log_form.is_valid():  
            us=log_form.cleaned_data.get('email')
            ps=log_form.cleaned_data.get('password')
            print(us)
            print(ps)
            user=authenticate(request,email=us,password=ps)
            print(user)
            if user: 
                login(request,user)
                print(request.user.is_faculty)
                if request.user.is_superuser == 1:
                    return redirect('ah')
                else:
                    return redirect('h')
                # else:
                #     return redirect('sh')
            else:
                return render(request,'login.html',{"form":log_form})
        else:
            return render(request,'login.html',{"form":log_form})  


class SugView(TemplateView):
    template_name="suggestions.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data']=Categorys.objects.all()
        return context

class SuggTextView(CreateView):
    template_name="suggtext.html"
    model=Categorys
    form_class=SuggestionForm
    success_url=reverse_lazy('st')


# def play_audioo(request, audio_id):
#     audio_recording = get_object_or_404(ScoreModel, pk=audio_id)
#     audio_file = audio_recording.audio
#     response = FileResponse(open(audio_file.path, 'rb'))
#     return response


class DeleteViewSug(View):
    def get(self,req,*args,**kwargs):
       id=kwargs.get('pk')
       dl=Categorys.objects.get(id=id)
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
            user=authenticate(request,email=request.user.email,password=current)
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
    model=Categorys
    form_class=SuggestionForm
    success_url=reverse_lazy('suggestions')   
   






from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from django.contrib.auth.views import (
    PasswordResetView, 
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView
)
from django.urls import reverse_lazy



class CustomPasswordResetView(PasswordResetView):
    template_name = 'password_reset.html'
    email_template_name = 'password_reset_email.html'
    success_url = reverse_lazy('password_reset_done')
    
class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'password_reset_done.html'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')
    
class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'password_reset_complete.html'
