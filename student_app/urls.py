from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static



urlpatterns =[
    path('shome/',StuHomeView.as_view(),name="sh"),
    path('exams-page/',AssignedExamStudentPageView.as_view(),name="stu_exam"),
    path('exam-result/',ResultStudentPageView.as_view(),name='result'),
    path('exam-main/<int:exam_id>/',ExamDetailView.as_view(),name='main-exam'),
    path('profile/',Profile.as_view(),name='pro'),
    path('sug/',SugView.as_view(),name='sug'),
    path('result/<int:pk>/',ResultView.as_view(),name='res'),
    path('cp/',ChangePasswordView.as_view(),name="cp"),
    path('logout/',LogOut.as_view(),name="logout"),
    path('proupdate/<int:pk>/',ProfileUpdateView.as_view(),name="proupd"),
    path('video/',Text.as_view(),name='text'),
    path('audio/',Audio.as_view(),name='audio'),
    path('noteview/',NotesListView.as_view(),name='noteview'),
    path('bot/',ChatBotView.as_view(),name='bot'),
    path('messagesview',MessageGetView.as_view(),name='msgview'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)