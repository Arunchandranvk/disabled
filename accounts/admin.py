from django.contrib import admin
from .models import *
from django.contrib.admin.models import LogEntry
from django.contrib.auth import get_user_model
from django.db import models

# class CustomLogEntry(LogEntry):
#     # Use your custom user model for the user field
#     CustUser = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, blank=True, null=True)

# # Register the custom LogEntry model with the admin site
# admin.site.register(CustomLogEntry)

# Register your models here.
admin.site.register(CustUser)
admin.site.register(Student)
admin.site.register(Faculty)
admin.site.register(Subject)
admin.site.register(AssignExam)
admin.site.register(ExamResult)
admin.site.register(Categorys)
admin.site.register(Class_Name)
admin.site.register(Exam)


