from django import forms
from accounts.models import Student


class ChangePasswordForm(forms.Form):
    current_password=forms.CharField(max_length=50,label="current password",widget=forms.PasswordInput(attrs={"placeholder":"Current Password","class":"form-control"}))
    new_password=forms.CharField(max_length=50,label="new password",widget=forms.PasswordInput(attrs={"placeholder":"New Password","class":"form-control"}))
    confirm_password=forms.CharField(max_length=50,label="confirm password",widget=forms.PasswordInput(attrs={"placeholder":"Confirm Password","class":"form-control"}))



class StudentFormProfile(forms.ModelForm):
     class Meta:
          model=Student
          fields=['first_name','last_name','email','img','gender','age','disability','accesstechnology']
          widgets={
               'first_name':forms.TextInput(attrs={"placeholder":"Firstname","class":"form-control","style":"border-radius: 0.75rem; "}),
               'last_name':forms.TextInput(attrs={"placeholder":"Lastname","class":"form-control","style":"border-radius: 0.75rem; "}),
               'email':forms.TextInput(attrs={"placeholder":"Email","class":"form-control","style":"border-radius: 0.75rem; "}),
               'gender':forms.RadioSelect(),
               'age':forms.NumberInput(attrs={"placeholder":"Age","class":"form-control","style":"border-radius: 0.75rem; "}),
          }



