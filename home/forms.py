from django import forms
from .models import Notes,Messages
from accounts.models import *

class NotesForm(forms.ModelForm):
    class Meta:
        model=Notes
        fields='__all__'

class MessageForm(forms.ModelForm):
    class Meta:
        model=Messages
        fields='__all__'

class ExamNameForm(forms.ModelForm):
    class Meta:
        model=Exam
        fields=['faculty','exam_name']

class QuestionsForm(forms.ModelForm):
    class Meta:
          model=ExamQuestions
          exclude=['exam']

    def __init__(self,*args,**kwargs):
        self.exam=kwargs.pop('exam',None)
        super().__init__(*args,**kwargs)

    def save(self, commit = True):
        instance = super().save(commit=False)
        if self.exam:
            instance.exam=Exam.objects.get(id=self.exam)
        if commit:
            instance.save()
        return instance




    