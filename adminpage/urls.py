from django.urls import path
from .views import *

urlpatterns = [
    path('adminhomepage/',AdminHome.as_view(),name='ah'),
    path('faculties/',FacultyList.as_view(),name='faculty'),
    path('students/',StudentsList.as_view(),name='students'),
    path('add-student/',AddStudent.as_view(),name='add-stu'),
    path('add-faculty/',AddFaculty.as_view(),name='add-fac'),
    path('add-subject/',AddSubject.as_view(),name='add-sub'),
    path('add-class/',AddClass.as_view(),name='add-cls'),
    path('remove-faculty/<int:pk>/',remove_faculty,name='del-fac'),
    path('remove-student/<int:pk>/',remove_student,name='del-stu'),
    path('remove-class/<int:pk>/',remove_class,name='del-cls'),
    path('remove-subject/<int:pk>/',remove_subject,name='del-sub'),
]
