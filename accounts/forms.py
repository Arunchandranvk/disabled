from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import *



class LogForm(forms.Form):
    email=forms.EmailField(widget=forms.EmailInput(attrs={"placeholder":"Email","class":"form-control","style":"border-radius: 0.75rem; "}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={"placeholder":"Password","class":"form-control","style":"border-radius: 0.75rem; "}))





class UserRegForm(UserCreationForm):
     class Meta:
          model=User
          fields=['username','password1']          
     
class QuesForm(forms.ModelForm):
     class Meta:
          model=ExamQuestions
          fields='__all__'

class SuggestionForm(forms.ModelForm):
     class Meta:
          model=Categorys
          fields='__all__'
     name=forms.CharField(widget=forms.TextInput(attrs={"Placeholder":"Name","class":"form-control","style":"padding:10px; "}) )    
     suggestion=forms.CharField(widget=forms.Textarea(attrs={"Placeholder":"Suggestion","class":"form-control","style":"padding:10px; "}) )    
     


# class QuesAnsForm(forms.ModelForm):
#      class Meta:
#           model=Answer
#           fields='__all__'
#      # question=forms.CharField(widget=forms.TypedMultipleChoiceField())
#      text=forms.CharField(widget=forms.TextInput(attrs={"Placeholder":"Option 1","class":"form-control","style":"border-radius: 0.75rem;padding:10px; "}) )    



