from django import forms
from .models import Notes,Messages

class NotesForm(forms.ModelForm):
    class Meta:
        model=Notes
        fields='__all__'
    file=forms.FileField(widget=forms.FileInput(attrs={"Placeholder":"Submit Notes","class":"form-control","style":"border-radius: 0.75rem;"}) )    
    # file=forms.FileField(widget=forms.FileInput(attrs={"Placeholder":"Submit Notes","class":"form-control","style":"border-radius: 0.75rem;"}) )    

class MessageForm(forms.ModelForm):
    class Meta:
        model=Messages
        fields='__all__'
